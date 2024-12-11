from pathlib import Path

from environ import Env

BASE_DIR = Path(__file__).resolve().parent.parent
env_path_list = [
    BASE_DIR / ".env",
    BASE_DIR / "../.env.django",
]

env = Env()

for env_path in env_path_list:
    if env_path.is_file():
        env.read_env(env_path, overwrite=True)

SECRET_KEY = env.str(
    "SECRET_KEY", default="django-insecure-test-key-do-not-use-in-production"
)

DEBUG = env.bool("DEBUG", default=True)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

INSTALLED_APPS = [
    # third party apps
    "daphne",
    # django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third party apps
    "corsheaders",
    "crispy_forms",
    "crispy_tailwind",
    "django_cotton",
    # local apps
    "pyhub_ai",
    # example apps
    "accounts",
    "example",
]

if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": env.db("DATABASE_URL", default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
}

if "sqlite" in DATABASES["default"]["ENGINE"]:
    if "OPTIONS" not in DATABASES["default"]:
        DATABASES["default"]["OPTIONS"] = {}
    # refs: https://gcollazo.com/optimal-sqlite-settings-for-django/
    DATABASES["default"]["OPTIONS"].update(
        {
            "init_command": (
                "PRAGMA foreign_keys = OFF;"
                "PRAGMA journal_mode = WAL;"
                "PRAGMA synchronous = NORMAL;"
                "PRAGMA busy_timeout = 5000;"
                "PRAGMA temp_store = MEMORY;"
                "PRAGMA mmap_size = 134217728;"
                "PRAGMA journal_size_limit = 67108864;"
                "PRAGMA cache_size = 2000;"
            ),
            # 위 가이드 대로 "IMMEDIATE"를 지정하니 SystemCheckError 발생
            # DatabaseBackend is using SQLite non-exclusive transactions
            #   HINT: Set settings.DATABASES["default"]["OPTIONS"]["transaction_mode"] to "EXCLUSIVE"
            "transaction_mode": "EXCLUSIVE",
        }
    )

AUTH_USER_MODEL = "accounts.User"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = env.str("LANGUAGE_CODE", default="ko-kr")
TIME_ZONE = env.str("TIME_ZONE", default="UTC")
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}

ASGI_APPLICATION = "mysite.asgi.application"

ROOT_URLCONF = "mysite.urls"

INTERNAL_IPS = env.list("INTERNAL_IPS", default=["127.0.0.1"])

# django-crispy-forms / crispy-tailwind
# https://github.com/django-crispy-forms/crispy-tailwind?tab=readme-ov-file#how-to-install
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"


# 주소 설정
#  - django-cors-headers : https://github.com/adamchainz/django-cors-headers?tab=readme-ov-file#configuration

# FE 주소: 로그인/로그아웃 후에 redirect 허용할 주소
#  - ex) fe.snu-aidatacamp.fly.dev
SUCCESS_URL_ALLOWED_HOSTS = env.list("SUCCESS_URL_ALLOWED_HOSTS", default=[])

# FE 주소 : fetch 요청을 허용할 출처(origin) 목록 (포트번호 포함)
#  - ex) https://fe.snu-aidatacamp.fly.dev
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])
# 정규표현식으로 fetch 요청을 허용할 ORIGIN 목록 지정
CORS_ALLOWED_ORIGIN_REGEXES = env.list("CORS_ALLOWED_ORIGIN_REGEXES", default=[])
# 모든 출처에 대해 fetch 요청을 허용할지 여부
CORS_ALLOW_ALL_ORIGINS = env.bool("CORS_ALLOW_ALL_ORIGINS", default=False)
# FE 단에서 fetch 요청 시에 인증정보(쿠키) 포함을 허용할 지 여부
CORS_ALLOW_CREDENTIALS = env.bool("CORS_ALLOW_CREDENTIALS", default=False)

# 세션/CSRF 쿠키를 허용할 도메인
#  - ex) ".snu-aidatacamp.fly.dev" : 하위 도메인까지 세션 쿠키 허용
SESSION_COOKIE_DOMAIN = env.str("SESSION_COOKIE_DOMAIN", default=None)
CSRF_COOKIE_DOMAIN = env.str("CSRF_COOKIE_DOMAIN", default=SESSION_COOKIE_DOMAIN)

# 세션 쿠키
SESSION_COOKIE_SAMESITE = env.str("SESSION_COOKIE_SAMESITE", default="Lax")
SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE", default=False)

# FE 주소: POST 요청 시에 CSRF
#  - 백엔드와 프론트엔드가 다른 도메인에서 운영될 때 필수
#  - 백엔드가 프록시(ex: nginx)를 경유해서 요청을 받을 때 scheme(http/https)가 다를 때에 요구받을 수 있음.
#    X-Forwarded-Proto 헤더로 original client protocol 전달 필요
#  - ex) https://fe.snu-aidatacamp.fly.dev
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])
