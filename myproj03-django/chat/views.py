from django.http import HttpResponse
from django.shortcuts import render
from django.utils.html import format_html


def index(request):
    return render(request, "chat/index.html")


def reply(request):

    if request.method == "POST":
        human_content = request.POST.get("content", "")
        ai_content = f"입력하신 메시지는 {len(human_content)} 글자입니다."

        return HttpResponse(format_html("<div>[Human] {}</div><div>[AI] {}</div>", human_content, ai_content));
    else:
        return HttpResponse("<div>허용하지 않는 메서드</div>")
