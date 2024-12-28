from typing import Iterator, List, Dict
from uuid import uuid4

from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views import View
from openai import OpenAI


def index(request):
    chat_messages = request.session.get("chat_messages", [])
    return render(
        request,
        "chat/index.html",
        {
            "chat_messages": chat_messages,
        },
    )


class ReplyView(View):
    system_prompt = "당신은 친절한 AI 어시스턴트입니다."

    def get_system_prompt(self) -> str:
        return self.system_prompt

    def get_chat_messages(self) -> List[Dict]:
        chat_messages = self.request.session.get("chat_messages", [])
        if not chat_messages:
            chat_messages = [
                {"role": "system", "content": self.get_system_prompt()},
            ]
        return chat_messages

    def make_response_chunks(self, human_content: str) -> Iterator[str]:
        human_message = {"role": "user", "content": human_content}

        chat_messages = self.get_chat_messages()
        chat_messages.append(human_message)

        yield render_to_string("chat/_chat_message.html", {"message": human_message})

        ai_message_id = "id_" + uuid4().hex  # dom id는 숫자로 시작하면 invalid
        ai_message = {"id": ai_message_id, "role": "assistant", "content": ""}

        yield render_to_string("chat/_chat_message.html", {"message": ai_message})

        client = OpenAI()

        completion = client.chat.completions.create(
            model="gpt-4o-mini", messages=chat_messages, stream=True
        )
        ai_content = ""
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                chunk_content = chunk.choices[0].delta.content
                ai_content += chunk_content
                ai_message["content"] = ai_content
                yield render_to_string(
                    "chat/_chat_message.html",
                    {
                        "message": ai_message,
                        "chunk": True,
                    },
                )

        # Iterator는 뷰 함수가 리턴되고 세션을 저장하는 미들웨어가 수행되고 나서 수행이 됩니다.
        # 그러니 세션 저장을 위해 명시적으로 session.save()를 호출해줘야만 합니다.
        chat_messages.append(ai_message)
        self.request.session["chat_messages"] = chat_messages
        self.request.session.modified = True
        self.request.session.save()

    def post(self, request) -> StreamingHttpResponse:
        # TODO: 값에 대한 유효성 검사는 장고 Form을 활용하면 편리.
        human_content = self.request.POST.get("content", "")

        response = StreamingHttpResponse(
            self.make_response_chunks(human_content), content_type="text/event-stream"
        )
        response["Cache-Control"] = "no-cache"
        response["X-Accel-Buffering"] = "no"
        return response


reply = ReplyView.as_view()
