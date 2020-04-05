"""context 에 sidebar, VERSION 추가."""
from book.nav import sidebar
from django.conf import settings


def settings_context(_request):
    """
    Context 보강.

    :param _request: request
    """
    return {"settings": settings, "sidebar": sidebar, "version": settings.VERSION}
