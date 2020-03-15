from ..settings import *
from ..settings import env


SECRET_KEY = env.str(
    "DJANGO_SECRET_KEY",
    default="vzMGloWEDX4CzAd3EqU3g2plcqrUG1tx0EAutfzBTdPspuJTke2fwuHEXgu0THny",
)
