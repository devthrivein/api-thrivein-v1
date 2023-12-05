from flask import jsonify, request
import bcrypt
from uuid import uuid4
from app.config.config import db
from datetime import datetime
from app.models.user_token import generate_token

def verify_login():
    # Periksa apakah permintaan POST "email" dan "password" ada
    if request.method == 'POST' and 'email' in request.get_json() and 'password' in request.get_json():
        # variabel untuk mendapatkan data dari formulir
        data = request.get_json()
        email = data.get('email')
        plain_password = data.get('password')

        # referensi ke koleksi "user" di Firestore
        accounts_ref = db.collection('user')

        # Query ke Firestore untuk mencari akun dengan email yang sesuai
        query = accounts_ref.where('user.email', '==', email)
        results = query.stream()

        # Jika ada akun dengan email yang sesuai
        for result in results:
            account_data = result.to_dict()
            hashed_password = account_data.get("password", "")

            # Periksa apakah plain_password sesuai dengan hashed_password
            if bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8')):
                
                # Generate token baru untuk user
                user_id = account_data['user']['user_id']
                user_name = account_data['user']['name']
                new_token = generate_token(user_id, user_name)

                # Update user's token di database
                user_ref = db.collection('user').document(user_id)
                user_ref.update({
                    'user.token': new_token
                })

                # Retrieve data user yang sudah di update
                updated_user_data = user_ref.get().to_dict()

                # variabel data store dan user di firestore untuk response
                store = account_data.get("store", None)
                user = updated_user_data.get("user", None)

                # Persiapkan response
                response = {
                    "store": store,
                    "user": user,
                }

                return jsonify(response), 201

        # Jika akun tidak ditemukan atau password salah
        response = {"error": "Incorrect email/password"}
        return jsonify(response), 401

    # Jika email atau password tidak disertakan dalam permintaan
    response = {"error": "Missing email or password in the request"}
    return jsonify(response), 400


def register():
    
    #user request body
    data = request.get_json()
    user_name = data.get('name')
    user_email = data.get('email')
    plain_password = data.get('password')
    user_phone = data.get('phone')
    #store request body
    store_name = data.get('store_name')
    store_email = data.get('store_email')
    store_phone = data.get('store_phone')
    address = data.get('address')
    type = data.get('store_type')

    # generate id user dengan uuid
    user_id = str(uuid4())

    # Hash kata sandi menggunakan bcrypt
    hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())

    # Query ke Firestore untuk memeriksa apakah email sudah terdaftar
    email_exists_query = db.collection('user').where('email', '==', user_email)
    email_exists_result = email_exists_query.stream()
    # Jika email sudah terdaftar, kembalikan respons dengan error message
    if len(list(email_exists_result)) > 0:
        response = {"error": "Email sudah terdaftar"}
        return jsonify(response), 400
    
    
    # Simpan informasi user ke Firestore
    user_ref = db.collection('user').document(str(user_id))
    token = generate_token(user_id, user_name)
    user_firestore_data = {
        'created_at': datetime.now(),
        'password': hashed_password.decode('utf-8'), 
        'user': {
            'email': user_email,
            'user_id' : user_id,
            'name': user_name,
            'phone': user_phone,
            'avatarUrl': '',
            'token': token
        },
        'store': {
            'store_name': store_name,
            'store_email': store_email,
            'store_phone': store_phone,
            'address': address,
            'type':type,
        }   
    }
    user_ref.set(user_firestore_data)

    # Exclude key 'password' untuk response
    response_data = {
        key: value for key, value in user_firestore_data.items() if key not in ['password', 'created_at']
    }
    # Persiapkan response
    response = response_data  

    return jsonify(response), 201  # Mengembalikan respons JSON
