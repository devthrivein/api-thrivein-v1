import firebase_admin
from firebase_admin import credentials, firestore
import os

# Path relatif dari config.py ke key.json
key_path = os.path.join(os.path.dirname(__file__), 'key.json')

# Inisialisasi Firestore
cred = credentials.Certificate(key_path)
firebase_admin.initialize_app(cred, {"projectId": "absolute-brook-402712"})
db = firestore.client()

class Config:
    SECRET_KEY = '' # our secret key

class JWTConfig:
    JWT_SECRET_KEY = '' # our secret key
    JWT_TOKEN_LOCATION = 'headers'
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
