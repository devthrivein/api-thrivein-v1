from flask import jsonify, request
from flask_jwt_extended import unset_jwt_cookies, get_jwt_identity
from app.config.config import db

def logout():

    # Unset JWT cookies to log the user out
    response = jsonify({"message": "Logout successful"})
    unset_jwt_cookies(response)

    return response, 200


def update_user():
    # mendapatkan user_id dari JWT
    current_user = get_jwt_identity()

    # variabel data untuk request dalam JSON
    data = request.get_json()

    # request body yang diperlukan (opsional)
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')

    # mendapatkan user document di firestore
    user_ref = db.collection('user').document(current_user)
    user_data = user_ref.get().to_dict()

    # Update the user data berdasarkan request body
    if name:
        user_data['user']['name'] = name
    if email:
        user_data['email'] = email
    if phone:
        user_data['user']['phone'] = phone

    # Save the updated user data ke firestore
    user_ref.update(user_data)

    # Return response
    response_data = {"message": "User profile updated successfully"}
    return jsonify(response_data), 200

def update_store():
    # mendapatkan user_id dari JWT
    current_user = get_jwt_identity()

    # variabel data untuk request JSON
    data = request.get_json()

    # request body yang diminta (opsional)
    store_name = data.get('store_name')
    store_email = data.get('store_email')
    store_phone = data.get('store_phone')
    address = data.get('address')
    store_type = data.get('type')

    #  mendapatkan user document dari Firestore
    store_ref = db.collection('user').document(current_user)
    store_data = store_ref.get().to_dict()

    # Update the store data ke firestore berdasarkan request body
    if store_name:
        store_data['store']['store_name'] = store_name
    if store_email:
        store_data['store']['store_email'] = store_email
    if store_phone:
        store_data['store']['store_phone'] = store_phone
    if address:
        store_data['store']['address'] = address
    if store_type:
        store_data['store']['type'] = store_type

    # Save the updated store data ke Firestore
    store_ref.update( store_data)

    # Return response
    response_data = {"message": "Store profile updated successfully"}
    return jsonify(response_data), 200