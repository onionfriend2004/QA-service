from .models import Tag, User
from django.core.cache import cache
from .utils import updateCache
import time

flag = False

def global_settings(request):
    global flag
    popular_tags = cache.get("popular_tags")
    best_members = cache.get("popular_users")
    if popular_tags is None:
        if not flag:
            flag = True
            updateCache()
            flag = False
        while flag:
            time.sleep(1)
        popular_tags = cache.get("popular_tags")
        best_members = cache.get("popular_users")

    return {
        "popular_tags": popular_tags,
        "popular_users": best_members,
    }