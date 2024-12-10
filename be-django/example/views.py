from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView, ListView

from example.forms import ChatRoomForm
from example.models import ChatRoom


class ChatRoomListView(LoginRequiredMixin, ListView):
    model = ChatRoom
    template_name = "example/index.html"

    def get(self, request, *args, **kwargs):
        ChatRoom.objects.get_or_create(
            user=request.user, defaults={"name": "상황극 채팅방 #1"}
        )
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


@login_required
def chat_room(request):
    obj = ChatRoom.objects.filter(user=request.user).first()
    if obj is None:
        raise Http404

    # is_ws = request.GET.get("protocol", "sse") == "ws"
    connect_url = f"/example/agent/chat/"
    template_name = "pyhub_ai/chat_room_sse.html"

    return render(
        request,
        template_name,
        {
            "connect_url": connect_url,
        },
    )


# class ChatRoomCreateView(LoginRequiredMixin, CreateView):
#     model = ChatRoom
#     form_class = ChatRoomForm
#     template_name = "form.html"
#
#     def form_valid(self, form):
#         obj = form.save(commit=False)
#         obj.user = self.request.user
#         return super().form_valid(form)
#
#     def get_success_url(self) -> str:
#         return self.object.get_absolute_url()


class ChatRoomUpdateView(LoginRequiredMixin, UpdateView):
    model = ChatRoom
    form_class = ChatRoomForm
    template_name = "form.html"
    success_url = reverse_lazy("example:index")

    def get_object(self, queryset=None):
        return ChatRoom.objects.filter(user=self.request.user).first()

    def form_valid(self, form):
        messages.success(self.request, "저장했습니다.")
        return super().form_valid(form)


#   def get_success_url(self) -> str:
#       return self.object.get_absolute_url()


# class ChatRoomDeleteView(LoginRequiredMixin, DeleteView):
#     model = ChatRoom
#     form_class = ChatRoomDeleteConfirmForm
#     template_name = "form.html"
#     success_url = reverse_lazy("example:index")
