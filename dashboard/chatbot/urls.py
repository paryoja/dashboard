"""Chatbot API URL."""

from django.urls import path

from . import views

app_name = "chatbot"
urlpatterns = [
    path("", views.AboutView.as_view(), name="index"),
    path("epl", views.EPLView.as_view(), name="epl"),
]
