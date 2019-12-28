from django.urls import path

from . import views

app_name = 'book'
urlpatterns = [
    path('', views.index, name='index'),
    path('study/slide/', views.slide, name='slide'),
    path('study/paper/', views.paper, name='paper'),
    path('study/colab/', views.colab, name='colab'),
    path('link/', views.link, name='link'),
    path('algorithm/', views.algorithm, name='algorithm'),
    path('law_search/', views.law_search, name='law_search'),
    path('lotto/', views.lotto, name='lotto'),
    path('export_lotto/', views.export_lotto, name='export_lotto'),
    path('wine/', views.wine, name='wine'),
    path('todo/', views.todo, name='todo'),
    path('investment/leading_stocks/', views.leading_stocks, name='leading_stocks'),
    path('investment/live_currency/', views.live_currency, name='live_currency'),
    path('investment/krx_price_query/', views.krx_price_query, name='krx_price_query'),
    path('idea/', views.idea, name='idea'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('query_chatbot/', views.query_chatbot, name='query_chatbot'),
    path('people/', views.people, name='people'),
]
