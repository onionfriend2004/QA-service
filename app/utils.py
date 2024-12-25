import time
import jwt
import uuid

from django.conf import settings

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