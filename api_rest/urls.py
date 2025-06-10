from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.get_users, name="get_all_users"),
    path("users/<str:nick>", views.get_by_nick),
    path("data/", views.user_manage)
]
    