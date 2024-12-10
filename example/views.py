from typing import Literal

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from example.forms import ChatRoomForm, ChatRoomDeleteConfirmForm
from example.models import ChatRoom


class ChatRoomListView(LoginRequiredMixin, ListView):
    model = ChatRoom
    template_name = "example/index.html"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


@login_required
def chat_room(request, pk: int):
    is_ws = request.GET.get("protocol", "sse") == "ws"

    qs = ChatRoom.objects.filter(pk=pk, user=request.user)
    if not qs.exists():
        raise Http404(f"ChatRoom #{pk} not found")

    agent_url = f"/example/agent/chat/{pk}/"

    if is_ws:
        connect_url = "/ws" + agent_url
        template_name = "pyhub_ai/chat_room_ws.html"
    else:
        connect_url = agent_url
        template_name = "pyhub_ai/chat_room_sse.html"

    return render(
        request,
        template_name,
        {
            "connect_url": connect_url,
        },
    )


class ChatRoomCreateView(LoginRequiredMixin, CreateView):
    model = ChatRoom
    form_class = ChatRoomForm
    template_name = "form.html"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return self.object.get_absolute_url()


class ChatRoomUpdateView(LoginRequiredMixin, UpdateView):
    model = ChatRoom
    form_class = ChatRoomForm
    template_name = "form.html"

    def get_success_url(self) -> str:
        return self.object.get_absolute_url()


class ChatRoomDeleteView(LoginRequiredMixin, DeleteView):
    model = ChatRoom
    form_class = ChatRoomDeleteConfirmForm
    template_name = "form.html"
    success_url = reverse_lazy("example:index")
