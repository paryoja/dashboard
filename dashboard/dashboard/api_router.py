"""API Router 등록."""

from book.api.views import InstagramTextViewSet, PokemonImageViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("pokemon", PokemonImageViewSet)
router.register("instagram", InstagramTextViewSet)
router.register("instagram_image", InstagramTextViewSet)

app_name = "api"
urlpatterns = router.urls
