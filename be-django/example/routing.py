from django.urls import path

from .agents import SituationChatView

# from .consumers import SituationChatConsumer


websocket_urlpatterns = [
    # path("ws/example/agent/chat/<int:pk>/", SituationChatConsumer.as_asgi()),
]

sse_urlpatterns = [
    path("agent/chat/", SituationChatView.as_view()),
]
