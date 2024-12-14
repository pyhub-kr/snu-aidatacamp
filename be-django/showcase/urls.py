from django.urls import path
from . import views

app_name = "showcase"

urlpatterns = [
    path("ajax/", views.ajax),
    path("ajax/<str:code>.json", views.ajax_data),
]
