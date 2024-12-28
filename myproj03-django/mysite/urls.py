# mysite/urls.py

from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

# 상위 URL Patterns
urlpatterns = [
    path("admin/", admin.site.urls),

    # hottrack.urls 내의 urlpatterns에 prefix로서 hottrack/을 추가
    path(route="hottrack/", view=include("hottrack.urls")),
    path(route="chat/", view=include("chat.urls")),

    # / 로 접근시 hottrack/ 주소로 페이지 이동
    path(route="", view=lambda request: redirect("/hottrack/")),
]
