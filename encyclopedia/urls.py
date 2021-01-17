from django.urls import path

from . import views

app_name = 'encyclopedia'
urlpatterns = [
    path("", views.index, name="index"),
    path("content/<str:name>", views.content, name="content"),
    path("search", views.search, name="search")
]
