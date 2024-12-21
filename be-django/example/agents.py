import json
import logging
from typing import Optional, Callable, Coroutine, Type, AsyncGenerator, Union

from asgiref.sync import sync_to_async
from django.template import Template as DjangoTemplate
from langchain_core.prompts import BasePromptTemplate
from pyhub_ai.models import Conversation
from pyhub_ai.specs import LLMModel
from pyhub_ai.views import AgentChatView

from .forms import MessageForm
from .models import ChatRoom


logger = logging.getLogger(__name__)


class SituationChatView(AgentChatView):
    form_class = MessageForm
    llm_timeout = 5

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

    def get_llm_model(self) -> LLMModel:
        if self.chat_room:
            return getattr(LLMModel, self.chat_room.llm_model)
        return super().get_llm_model()

    def get_llm_temperature(self) -> float:
        if self.chat_room:
            return self.chat_room.llm_temperature
        return super().get_llm_temperature()

    async def aget_llm_system_prompt_template(self) -> str:
        if self.chat_room:
            return self.chat_room.llm_system_prompt_template
        return await super().aget_llm_system_prompt_template()

    async def aget_llm_first_user_message(self) -> str:
        if self.chat_room:
            return self.chat_room.llm_first_user_message_template
        return await super().aget_llm_first_user_message()

    async def get_conversation(self) -> Optional[Conversation]:
        def get():
            if self.chat_room:
                return self.chat_room.conversation
            return None

        return await sync_to_async(get)()

    async def make_stream_response(
        self, coroutine_producer: Coroutine
    ) -> AsyncGenerator[str, None]:
        async_gen = super().make_stream_response(coroutine_producer)

        if self.render_format != "json":
            async for chunk in async_gen:
                yield chunk

        else:
            # 클라이언트 단에서 보다 쉬운 응답 처리를 위해
            # JSON 응답에 한해서 리스트로서 응답합니다.

            response_dict = {}

            async for chunk in async_gen:
                try:
                    obj = json.loads(chunk)
                except json.JSONDecodeError as e:
                    logger.warning(e)
                else:
                    if obj["id"] not in response_dict:
                        response_dict[obj["id"]] = obj.copy()
                    else:
                        current = response_dict[obj["id"]]
                        current_content = current.get("content") or ""
                        current["content"] = current_content + (obj["content"] or "")

            yield json.dumps(list(response_dict.values()), ensure_ascii=False)
