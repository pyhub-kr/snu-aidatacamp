from django.contrib import admin

from .forms import ChatRoomForm
from .models import ChatRoom


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name")
    form = ChatRoomForm

    def save_model(self, request, obj, form, change):
        if not change:  # 새로운 객체를 생성하는 경우
            obj.user = request.user
        super().save_model(request, obj, form, change)
