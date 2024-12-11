# 서울대학교 웹앱개발 겨울캠프 2024 백엔드 저장소

## 핵심 언어/라이브러리

+ `django-pyhub-ai` : 자체 라이브러리
    - [관련 튜토리얼](https://django-pyhub-ai.readthedocs.io)
+ `Python` 3.13
+ `Django` 5.1
+ `HTMX`
+ `django-crispy-forms` : 폼 처리
+ `LangChain`
+ `OpenAI` API

## 설정된 환경변수

```
OPENAI_API_KEY=OPENAI_API_키

DATABASE_URL=데이터베이스_접근정보

DEBUG=0

ALLOWED_HOSTS=localhost,aidatacamp.pyhub.kr
SUCCESS_URL_ALLOWED_HOSTS=fe.aidatacamp.pyhub.kr:3000,fe.aidatacamp.pyhub.kr:5500,fe.aidatacamp.pyhub.kr:5173
CSRF_TRUSTED_ORIGINS=https://aidatacamp.pyhub.kr,http://fe.aidatacamp.pyhub.kr:3000,http://fe.aidatacamp.pyhub.kr:5500,http://fe.aidatacamp.pyhub.kr:5173
CORS_ALLOWED_ORIGINS=http://fe.aidatacamp.pyhub.kr:3000,http://fe.aidatacamp.pyhub.kr:5500,http://fe.aidatacamp.pyhub.kr:5173
CORS_ALLOW_ALL_ORIGINS=0
CORS_ALLOW_CREDENTIALS=1

CSRF_COOKIE_DOMAIN=.aidatacamp.pyhub.kr
SESSION_COOKIE_DOMAIN=.aidatacamp.pyhub.kr

SESSION_COOKIE_SAMESITE="None"
SESSION_COOKIE_SECURE=1
```
