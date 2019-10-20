from django.urls import path

from . import views

app_name = 'book'
urlpatterns = [
    path('', views.index, name='index'),
    path('deep_learning', views.deep_learning, name='deep_learning'),
    path('link', views.link, name='link'),
    path('algorithm', views.algorithm, name='algorithm'),
    path('invest', views.invest, name='invest'),
    path('law_search', views.law_search, name='law_search'),
    path('wine', views.wine, name='wine'),
    path('todo', views.todo, name='todo'),
]
