# utils.py
import random
import string
from .models import URLMap


def get_unique_short_id(length=6):
    while True:
        short_id = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id
