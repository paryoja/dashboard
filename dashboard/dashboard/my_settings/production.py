from ..settings import *  # noqa F401
from ..settings import env

SECRET_KEY = env.str("DJANGO_SECRET_KEY")
