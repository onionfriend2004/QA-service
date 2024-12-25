import time
import jwt
import uuid

from django.conf import settings
from django.core.cache import cache

from app.models import Tag, Profile

def get_centrifugo_info():
    secret = settings.CENTRIFUGO_SECRET_KEY
    ws_url = settings.CENTRIFUGO_WS_URL

    anonymous_user_id = str(uuid.uuid4())

    claims = {
        "sub": anonymous_user_id,
        "exp": int(time.time()) + 5 * 60
    }

    token = jwt.encode(claims, secret, algorithm="HS256")
    return {
        'token': token,
        'ws_url': ws_url
    }

def updateTags():
    popular_tags = Tag.objects.popular_tags()
    cache.set("popular_tags", list(popular_tags), 60 * 60 * 24)  # Кэшируем на сутки

def updateUsers():
    popular_users = Profile.objects.popular_users()
    cache.set("popular_users", list(popular_users), 60 * 60 * 24)  # Кэшируем на сутки

def updateCache():
    updateTags()
    updateUsers()
