from django.http import HttpResponse
from django.shortcuts import render
from django.utils.html import format_html
from openai import OpenAI


def index(request):
    return render(request, "chat/index.html")


def reply(request):

    if request.method == "POST":
        human_content = request.POST.get("content", "")

        client = OpenAI()

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 친절한 AI 어시스턴트입니다."},
                {"role": "user", "content": human_content},
            ],
        )
        ai_content = completion.choices[0].message.content

        return HttpResponse(
            format_html(
                "<div>[Human] {}</div><div>[AI] {}</div>", human_content, ai_content
            )
        )
    else:
        return HttpResponse("<div>허용하지 않는 메서드</div>")
