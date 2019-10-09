from django.urls import path

from . import views

app_name = 'book'
urlpatterns = [
    path('', views.index, name='index'),
    path('link', views.link, name='link'),
    path('algorithm', views.algorithm, name='algorithm'),
    path('invest', views.invest, name='invest'),
    path('law_search', views.law_search, name='law_search'),
]
