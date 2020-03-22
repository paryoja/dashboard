from book.api.views import PokemonImageViewSet
from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", PokemonImageViewSet)

app_name = "api"
urlpatterns = router.urls
