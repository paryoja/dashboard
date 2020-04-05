"""테스트 환경."""
from ..settings import *  # noqa F401
# noinspection PyUnresolvedReferences
from ..settings import env

SECRET_KEY = env.str(
    "DJANGO_SECRET_KEY",
    default="vzMGloWEDX4CzAd3EqU3g2plcqrUG1tx0EAutfzBTdPspuJTke2fwuHEXgu0THny",
)
