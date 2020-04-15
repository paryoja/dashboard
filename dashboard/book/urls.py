"""Book 의 URL."""

from django.urls import path

from . import views_user
from .views import krx, people, views, views_api, views_class

app_name = "book"

# Home
urlpatterns = [
    path("", views_class.IndexTemplateView.as_view(), name="index",),
]

# Study
urlpatterns += [
    path("study/slide/", views_class.SlideTemplateView.as_view(), name="slide",),
    path("study/paper/", views_class.PaperListViwew.as_view(), name="paper",),
    path("study/colab/", views_class.ColabTemplateView.as_view(), name="colab",),
]

# Pokemon
urlpatterns += [
    path("pokemon/", views.pokemon, name="pokemon_classification"),
    path("pokemon/<int:page>", views.pokemon, name="pokemon_classification"),
    path("pokemon_result/", views.pokemon_result, name="pokemon_result"),
    path("pokemon_result/<int:page>", views.pokemon_result, name="pokemon_result"),
    path("pokemon/sorted/", views.pokemon_sorted, name="pokemon_sorted"),
    path(
        "pokemon_export/<str:classified>/<int:page>",
        views.pokemon_export,
        name="pokemon_export",
    ),
    path("pokemon/relabel", views.pokemon_relabel, name="pokemon_relabel"),
    path(
        "pokemon/classification_api",
        views_api.pokemon_classification_api,
        name="pokemon_classification_api",
    ),
]

# Corona
urlpatterns += [
    path("corona", views.corona, name="corona"),
]

# Chatbot
urlpatterns += [
    path("chatbot/", views_class.ChatbotTemplateView.as_view(), name="chatbot"),
    path("query_chatbot/", views.query_chatbot, name="query_chatbot"),
    path("query/", views_class.QueryView.as_view(), name="query"),
]

# Link
urlpatterns += [
    path("web_stack/", views_class.WebStackListView.as_view(), name="web_stack",),
    path("link/", views_class.BookmarkListView.as_view(), name="link",),
]

# Investment
urlpatterns += [
    path(
        "investment/leading_stocks/",
        views_class.LeadingStockTemplateView.as_view(),
        name="leading_stocks",
    ),
    path("investment/currency_change/", views.currency_change, name="currency_change"),
    path("investment/krx_price_query/", krx.krx_price_query, name="krx_price_query"),
    path("real_estate/", views.real_estate, name="real_estate"),
    path("lotto/", views.lotto, name="lotto"),
    path("export_lotto/", views.export_lotto, name="export_lotto"),
    path(
        "recommend_book/",
        views_class.RecommendBookListView.as_view(),
        name="recommend_book",
    ),
]

# ETC
urlpatterns += [
    path("food/", views.food, name="food"),
    path("wine/", views_class.WineListView.as_view(), name="wine",),
    path("law_search/", views.law_search, name="law_search"),
    path("todo/", views_class.TodoTemplateView.as_view(), name="todo"),
    path("idea/", views_class.IdeaTemplateView.as_view(), name="idea"),
]

# People
urlpatterns += [
    path("people/", people.people, name="people"),
    path("people_result/", people.people_result, name="people_result"),
    path("people_result/<int:page>", people.people_result, name="people_result"),
    path(
        "people_result/download/<str:selected>/<int:page>",
        people.people_result_download,
        name="people_result_download",
    ),
    path(
        "people/high_expectation/",
        people.people_high_expectation,
        name="people_high_expectation",
    ),
    path("people/people_links/", people.people_links, name="people_links"),
    path("people/relabel", views.relabel, name="people_relabel"),
    path(
        "people/classification_api",
        views_api.people_classification_api,
        name="people_classification_api",
    ),
    path("people/get_id", views_api.get_id, name="people_get_id"),
]

# Image api
urlpatterns += [
    path("add_image/", views.image, name="add_image"),
    path("add_image/<str:data_type>", views.image, name="add_image"),
    path("add_user/", views.add_user, name="add_user"),
    path("image/api/<str:method>", views_api.image, name="image"),
    path("image/api/<str:method>/<str:image_type>", views_api.image, name="image"),
    path("rating/api", views_api.set_rating, name="rating_api"),
]

# session
urlpatterns += [
    path("login/", views_user.BookLoginView.as_view(), name="login"),
    path("logout/", views_user.BookLogoutView.as_view(), name="logout"),
]

# Invalid
urlpatterns += [
    path("algorithm/", views_class.AlgorithmTemplateView.as_view(), name="algorithm",),
]
