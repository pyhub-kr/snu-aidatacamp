import json
from urllib.request import urlopen

from django.db.models import QuerySet, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

from hottrack.models import Song


# def index(request: HttpRequest) -> HttpResponse:
#     query = request.GET.get("query", "").strip()
#
#     #
#     # 외부 데이터를 로딩해서 보여주기
#     #
#     # melon_chart_url = "https://raw.githubusercontent.com/pyhub-kr/dump-data/main/melon/melon-20230910.json"
#     # json_string = urlopen(melon_chart_url).read().decode("utf-8")
#     # # 외부 필드명을 그대로 쓰기보다, 내부적으로 사용하는 필드명으로 변경하고, 필요한 메서드를 추가합니다.
#     # song_list = [Song.from_dict(song_dict) for song_dict in json.loads(json_string)]
#
#     # if query:
#     #     song_list = [
#     #         song
#     #         for song in song_list
#     #         if (
#     #             (query in song.name)
#     #             or (query in song.artist_name)
#     #             or (query in song.album_name)
#     #             # or (query in song.lyrics)
#     #         )
#     #     ]
#
#     #
#     # 데이터 베이스 데이터를 조회해서 보여주기
#     #
#     song_qs: QuerySet = Song.objects.all()
#
#     if query:
#         song_qs = song_qs.filter(
#           Q(name__icontains=query)
#           | Q(artist_name__icontains=query)
#           | Q(album_name__icontains=query)
#         )
#
#     return render(
#         request=request,
#         template_name="hottrack/index.html",
#         context={
#             "song_list": song_qs,
#             "query": query,
#         },
#     )
#


class SongListView(ListView):
    model = Song
    template_name = "hottrack/index.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.query = ""  # instance 변수는 생성자에 정의합니다.

    def get_queryset(self):
        qs = super().get_queryset()
        self.query = self.request.GET.get("query", "").strip()
        if self.query:
            qs = qs.filter(
              Q(name__icontains=self.query)
              | Q(artist_name__icontains=self.query)
              | Q(album_name__icontains=self.query)
            )
        return qs

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["query"] = self.query
        return context_data


# 검색 지원 X
index = SongListView.as_view()
