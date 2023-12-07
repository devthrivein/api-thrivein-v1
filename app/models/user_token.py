import jwt
from datetime import datetime, timedelta
from flask import current_app as app

def generate_token(user_id, name):
    payload = {
        'sub': user_id,
        'name': name,  
        'exp': datetime.utcnow() + timedelta(days=365)  # Atur waktu kadaluwarsa token
    }
    token = jwt.encode(payload, app.config['JWT_SECRET_KEY'], algorithm='HS256')
    return token

def generate_token_admin(admin_id, admin_name):
    payload = {
        'sub': admin_id,
        'name': admin_name,  
        'exp': datetime.utcnow() + timedelta(days=1)  # Atur waktu kadaluwarsa token
    }
    token = jwt.encode(payload, app.config['JWT_SECRET_KEY'], algorithm='HS256')
    return token