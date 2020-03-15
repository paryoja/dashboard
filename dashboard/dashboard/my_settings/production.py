from ..settings import *
from ..settings import env

SECRET_KEY = env.str("DJANGO_SECRET_KEY")
