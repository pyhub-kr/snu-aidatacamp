# hottrack/apps.py

from django.apps import AppConfig

class HottrackConfig(AppConfig):
    # 디폴트 기본키는 8바이트 크기를 가집니다.
    default_auto_field = "django.db.models.BigAutoField"
    name = "hottrack"
    # ADDED : admin 페이지에서 지정 이름으로 보여집니다.
    verbose_name = "핫트랙"
