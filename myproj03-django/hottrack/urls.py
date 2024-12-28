from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
]

# nanodjango
# @app.route("/")
# def index(request):
#     pass