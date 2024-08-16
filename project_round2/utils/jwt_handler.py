import jwt
from datetime import datetime, timedelta
from config import Config

def generate_jwt_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=1)  
    }
    access_token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')

    refresh_payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=30)  
    }
    refresh_token = jwt.encode(refresh_payload, Config.JWT_SECRET_KEY, algorithm='HS256')

    return access_token, refresh_token

def verify_jwt_token(token):
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
