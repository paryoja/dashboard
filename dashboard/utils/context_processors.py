from book.nav import sidebar
from django.conf import settings


def settings_context(_request):
    return {"settings": settings, "sidebar": sidebar, "version": settings.VERSION}
