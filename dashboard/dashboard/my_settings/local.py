# noinspection PyUnresolvedReferences
from ..settings import *  # noqa F401
from ..settings import env

SECRET_KEY = env.str(
    "DJANGO_SECRET_KEY",
    default="nyL82uqeMOVK4VrLyafHXVNQS2dt2GD4K07CIJAPyrh2ux2FXmPms6EI1jEdDe4E",
)

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
INSTALLED_APPS += ["debug_toolbar", "django_extensions"]  # noqa F405

# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa F405

# https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}

# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2", "172.23.0.7"]

if env("USE_DOCKER") == "yes":
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [ip[:-1] + "1" for ip in ips]
