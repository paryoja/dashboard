"""API Router 등록."""

from book.api import views
from chatbot.api.views import WikiViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("pokemon", views.PokemonImageViewSet)
router.register("instagram", views.InstagramTextViewSet)
router.register(
    "instagram_image", views.InstagramImageViewSet, basename="instagram_image"
)
router.register("wiki", WikiViewSet)

app_name = "api"
urlpatterns = router.urls
