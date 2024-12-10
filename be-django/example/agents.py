from typing import Optional, Callable, Coroutine, Type

from asgiref.sync import sync_to_async
from pyhub_ai.models import Conversation
from pyhub_ai.specs import LLMModel
from pyhub_ai.views import AgentChatView

from .forms import MessageForm
from .models import ChatRoom


class SituationChatView(AgentChatView):
    form_class = MessageForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chat_room: Optional[ChatRoom] = None

    async def chat_setup(self, send_func: Callable[[str], Coroutine]) -> None:
        current_user = await self.get_user()
        if current_user:
            # pk = self.kwargs["pk"]
            # qs = ChatRoom.objects.filter(pk=pk, user=current_user)
            qs = ChatRoom.objects.filter(user=current_user)
            self.chat_room = await qs.afirst()

        await super().chat_setup(send_func)

    def get_llm_model(self) -> Type[LLMModel]:
        if self.chat_room:
            return LLMModel[self.chat_room.llm_model]
        return super().get_llm_model()

    def get_llm_temperature(self) -> float:
        if self.chat_room:
            return self.chat_room.llm_temperature
        return super().get_llm_temperature()

    def get_llm_system_prompt_template(self) -> str:
        if self.chat_room:
            return self.chat_room.llm_system_prompt_template
        return super().get_llm_system_prompt_template()

    def get_llm_first_user_message(self) -> str:
        if self.chat_room:
            return self.chat_room.llm_first_user_message_template
        return super().get_llm_first_user_message()

    async def get_conversation(self) -> Optional[Conversation]:
        def get():
            if self.chat_room:
                return self.chat_room.conversation
            return None

        return await sync_to_async(get)()
