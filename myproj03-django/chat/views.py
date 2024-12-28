from django.http import HttpResponse
from django.shortcuts import render
from django.utils.html import format_html
from openai import OpenAI


def index(request):
    chat_messages = request.session.get('chat_messages', [])
    return render(request, "chat/index.html", {
        "chat_messages": chat_messages,
    })


def reply(request):

    if request.method == "POST":
        # TODO: 값에 대한 유효성 검사는 장고 Form을 활용하면 편리.
        human_content = request.POST.get("content", "")

        chat_messages = request.session.get('chat_messages', [])
        if not chat_messages:
            chat_messages = [
                {"role": "system", "content": "당신은 친절한 AI 어시스턴트입니다."},
            ]
        chat_messages.append({"role": "user", "content": human_content})

        client = OpenAI()

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=chat_messages,
        )
        ai_content = completion.choices[0].message.content
        chat_messages.append({ "role": "assistant", "content": ai_content })

        request.session['chat_messages'] = chat_messages

        return HttpResponse(
            format_html(
                "<div>[Human] {}</div><div>[AI] {}</div>", human_content, ai_content
            )
        )
    else:
        return HttpResponse("<div>허용하지 않는 메서드</div>")
