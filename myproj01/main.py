import json
from django.shortcuts import render
from nanodjango import Django

app = Django()

@app.route("/")
def index(request):
#   return render(request, "index.html")

    with open("./data/data.json", "rt", encoding="utf-8") as f:
        page_list = json.loads(f.read())

    page_dict = {page["id"]: page for page in page_list}

    current_page_id = request.GET.get("page_id", "js")
    current_page = page_dict[current_page_id]

    # 템플릿은 단순히 표현에만 관심을 두도록 제한.
    button_colors = [
        "dodgerblue",
        "darkorange",
        "mediumseagreen",
        "mediumpurple",
        "tomato",
    ]

    return render(
        request,
        "home.html",
        {
            "current_page_id": current_page_id,
            "page_dict": page_dict,
            "current_page": current_page,
            "button_colors": button_colors,
        },
    )


@app.route("/home")
def home(request):
    # return render(request, "index.html")
    return "Hello Home"
