from django.urls import path

from .views import *

app_name = 'book'
urlpatterns = [
    path('', index, name='index'),
    path('cbvList', BoardsListClassView.as_view()),
    path('fbvList', BoardsListFunctionView),
]
