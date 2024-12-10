from django.urls import path

from .routing import sse_urlpatterns
from . import views

app_name = "example"

urlpatterns = [
    path("", views.ChatRoomListView.as_view(), name="index"),
    # chat room
    path("chat/<int:pk>/", views.chat_room, name="situation-chat-room"),
    path(
        "chat/new/", views.ChatRoomCreateView.as_view(), name="situation-chat-room-new"
    ),
    path(
        "chat/<int:pk>/edit/",
        views.ChatRoomUpdateView.as_view(),
        name="situation-chat-room-edit",
    ),
    path(
        "chat/<int:pk>/delete/",
        views.ChatRoomDeleteView.as_view(),
        name="situation-chat-room-delete",
    ),
]

urlpatterns += sse_urlpatterns
