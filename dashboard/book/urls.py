from django.urls import path

from . import views

app_name = 'book'
urlpatterns = [
    path('', views.index, name='index'),
    path('link', views.link, name='link'),
    path('algorithm', views.algorithm, name='algorithm'),
]
