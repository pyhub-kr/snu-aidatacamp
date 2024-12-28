from typing import Iterator

from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.utils.html import format_html
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


def reply(request):

    if request.method == "POST":
        # TODO: 값에 대한 유효성 검사는 장고 Form을 활용하면 편리.
        human_content = request.POST.get("content", "")

        chat_messages = request.session.get("chat_messages", [])
        if not chat_messages:
            chat_messages = [
                {"role": "system", "content": "당신은 친절한 AI 어시스턴트입니다."},
            ]
        chat_messages.append({"role": "user", "content": human_content})

        client = OpenAI()

        completion = client.chat.completions.create(
            model="gpt-4o-mini", messages=chat_messages, stream=True
        )

        def make_chunks() -> Iterator[str]:
            # div를 닫지 않았지만, 웹페이지에 적용되면 브라우저에 의해 자동으로 닫힙니다.
            yield format_html("<div>[Human] {}</div><div>[AI] ", human_content)

            ai_content = ""
            for chunk in completion:
                if chunk.choices[0].delta.content is not None:
                    chunk_content = chunk.choices[0].delta.content
                    ai_content += chunk_content
                    yield chunk_content

            # Iterator는 뷰 함수가 리턴되고 세션을 저장하는 미들웨어가 수행되고 나서 수행이 됩니다.
            # 그러니 세션 저장을 위해 명시적으로 session.save()를 호출해줘야만 합니다.
            chat_messages.append({"role": "assistant", "content": ai_content})
            request.session["chat_messages"] = chat_messages
            request.session.modified = True
            request.session.save()

            yield "</div>"

        response = StreamingHttpResponse(
            make_chunks(), content_type="text/event-stream"
        )
        response["Cache-Control"] = "no-cache"
        response["X-Accel-Buffering"] = "no"
        return response
    else:
        return HttpResponse("<div>허용하지 않는 메서드</div>")
