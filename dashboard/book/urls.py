from django.urls import path

from . import views
from . import views_api
from . import views_user

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
    path('people_result/', views.people_result, name='people_result'),
    path('people_result/<int:page>', views.people_result, name='people_result'),
    path('people_result/download/<str:selected>', views.people_result_download, name='people_result_download'),

    path('real_estate/', views.real_estate, name='real_estate'),
    path('recommend_book/', views.recommend_book, name='recommend_book'),
    path('food/', views.food, name='food'),
    path('pokemon/', views.pokemon, name='pokemon_classification'),
    path('pokemon/<int:page>', views.pokemon, name='pokemon_classification'),
    path('pokemon_result/', views.pokemon_result, name='pokemon_result'),
    path('pokemon_result/<int:page>', views.pokemon_result, name='pokemon_result'),
    path('pokemon_export/<str:classified>', views.pokemon_export, name='pokemon_export'),
    path('add_image/', views.add_image, name='add_image'),
    path('add_image/<str:data_type>', views.add_image, name='add_image'),
    path('login/', views_user.BookLoginView.as_view(), name='login'),
    path('logout/', views_user.BookLogoutView.as_view(), name='logout'),
    path('rating/api', views_api.set_rating, name='rating_api'),
]
