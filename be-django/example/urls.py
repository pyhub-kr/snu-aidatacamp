from django.urls import path

from .routing import sse_urlpatterns
from . import views

app_name = "example"

urlpatterns = [
    path("", views.ChatRoomListView.as_view(), name="index"),
    path("chat/", views.chat_room, name="chat-room"),
    path("edit/", views.ChatRoomUpdateView.as_view(), name="edit"),
]

urlpatterns += sse_urlpatterns
