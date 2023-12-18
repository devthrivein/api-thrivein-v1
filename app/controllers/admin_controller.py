from flask import jsonify, request
from app.config.config import db
from datetime import datetime
from firebase_admin import firestore
from app.models.user_token import generate_token_admin
from uuid import uuid4
import bcrypt

def update_status_order(order_id):
    # variabel data untuk request json
    data = request.get_json()

    # request body yang diperlukan 
    status = data.get('status')

    # Query firestore untuk mendaptkan order dari user berdasarkan order_id
    order_ref_query = db.collection('order').where("order_id", "==", order_id)

    # mendapatkan hasil dari query diatas
    order_results = list(order_ref_query.stream())

    if not order_results:
        return jsonify({"error": "Order not found"}), 404

    # Update document yang bersangkutan
    for order_doc in order_results:
        order_doc_ref = db.collection('order').document(order_doc.id)
        order_data_update = {
            "status": status,
        }
        order_doc_ref.update(order_data_update)

    response_update = {"message": "Status Updated"}
    return jsonify(response_update), 201

def get_all_order():
    # query Parameters untuk pagination 
    size = request.args.get('size', type=int)
    page = request.args.get('page', type=int)

    is_order_now = True
    #query firestore untuk mendapatkan detail history order berdasarkan 'order_id'
    order_ref = db.collection('order').where("is_order_now", "==" , is_order_now )
    query = order_ref.limit(size).offset((page - 1) * size)
    detail_result = query.stream()

    all_order = []
    for result in detail_result:
        all_order_data = result.to_dict()
        all_order_info = {
            'order_id': all_order_data.get('order_id'),
            'title': all_order_data.get('title'),
            'transaction_date': all_order_data.get('transaction_date'),
            'status': all_order_data.get('status'),
            'name': all_order_data.get('name')
        }
        all_order.append(all_order_info)
    
    #return response
    response = {"meta":page, 'order_data': all_order}
    return jsonify(response), 200

def update_banner(id):
    # variabel data untuk request json
    data = request.get_json()

    # request body yang diperlukan 
    banner_txt = data.get('banner_txt')
    banner_url = data.get('banner_url')
    title = data.get('title')

    # Query firestore untuk mendaptkan order dari user berdasarkan order_id
    banner_ref_query = db.collection('banners').where("id", "==", id)

    # mendapatkan hasil dari query diatas
    order_results = list(banner_ref_query.stream())

    if not order_results:
        return jsonify({"error": "banner not found"}), 404
    
    # Update document yang bersangkutan
    for banner_doc in order_results:
        banner_doc_ref = db.collection('banners').document(banner_doc.id)
        banner_data_update = {
            "banner_txt": banner_txt,
            "banner_url": banner_url,
            "title": title
        }
        banner_doc_ref.update(banner_data_update)

    response_update = {"message": "banner Updated"}
    return jsonify(response_update), 201



def get_order_count():
    # Membuat filter untuk setiap kondisi
    filters = [
        {'is_order_now': True, 'status': 'baru'},
        {'is_order_now': True, 'status': 'diproses'},
        {'is_order_now': True, 'status': 'selesai'},
    ]

    # Menginisialisasi dictionary untuk menyimpan hasil
    order_counts = {}

    # Melakukan query dan menghitung jumlah untuk setiap kondisi
    for condition in filters:
        count = count_orders(condition)
        order_counts[condition['status']] = count

    # Mengembalikan respons dalam bentuk JSON
    return jsonify(order_counts), 200

def count_orders(condition):
    # Melakukan query Firestore untuk menghitung jumlah dokumen berdasarkan kondisi
    order_ref_query = db.collection('order').where("is_order_now", "==", condition['is_order_now']).where("status", "==", condition['status'])
    order_count = len(list(order_ref_query.stream()))

    return order_count


def get_user_count():
    # Melakukan query Firestore untuk mendapatkan seluruh dokumen pada collection 'user'
    user_ref = db.collection('user')
    user_count = len(list(user_ref.stream()))

    # Mengembalikan respons dalam bentuk JSON
    return jsonify({"user": user_count}), 200

def admin_get_order(order_id):
    #query firestore untuk mendapatkan detail history order berdasarkan 'order_id'
    detail_order_ref = db.collection('order').document(order_id)
    detail_result = detail_order_ref.get().to_dict()

    # Exclude key yang tidak perlu untuk respons
    excluded_fields = ['discount','is_order_now','payment_method','user_id', 'consultation_id', 'address', 'total_order', 'total_pay', 'invoice']

    # return response
    response = {key: value for key, value in detail_result.items() if key not in excluded_fields}
    return jsonify(response), 200

def generate_article_id():
    # Mendapatkan 'article_id' terakhir yang terdapat pada Firestore
    last_article_ref = db.collection('articles').order_by('article_id', direction=firestore.Query.DESCENDING).limit(1)
    last_article = next(last_article_ref.stream(), None)

    # Ekstrak order_id terakhir
    last_article_id = last_article.get('article_id') if last_article else None

    # Generate order_id baru
    if last_article_id:
        order_number = int(last_article_id[1:]) + 1
        new_article_id = f"A{order_number:03}"
    else:
        new_article_id = "A001"

    return new_article_id

def post_article(): 
    #request body 
    data = request.get_json()
    banner_url = data.get('banner_url')
    content = data.get('content')
    title = data.get('title')

    article_id = generate_article_id()

    article_ref = db.collection('articles').document(str(article_id))
    article_firestore_data = {
        'article_id': article_id,
        'banner_url' : banner_url,
        'content': content,
        'title': title,
        'uploaded_date': datetime.now()
    }
    article_ref.set(article_firestore_data)

    response_article = {"message": "Article Posted"}
    return jsonify(response_article), 201

def update_services(service_id):
    # variabel data untuk request json
    data = request.get_json()

    # request body yang diperlukan 
    description = data.get('description')
    icon_url = data.get('icon_url')
    title = data.get('title')

    # Query firestore untuk mendaptkan layanan berdasarkan service_id
    services_ref_query = db.collection('services').where("service_id", "==", service_id)

    # mendapatkan hasil dari query diatas
    services_results = list(services_ref_query.stream())

    if not services_results:
        return jsonify({"error": "Service not found"}), 404
    
    # Update document yang bersangkutan
    for services_doc in services_results:
        services_doc_ref = db.collection('services').document(services_doc.id)
        services_data_update = {
            "description": description,
            "icon_url": icon_url,
            "title": title
        }
        services_doc_ref.update(services_data_update)

    response_update = {"message": "Services Updated"}
    return jsonify(response_update), 201

def admin_get_services(service_id):
    #query firestore untuk mendapatkan detail history order berdasarkan 'service_id'
    detail_service_ref = db.collection('services').document(service_id)
    detail_result = detail_service_ref.get().to_dict()

    # Exclude key yang tidak perlu untuk respons
    excluded_fields = ['category','service_id']

    # return response
    response = {key: value for key, value in detail_result.items() if key not in excluded_fields}
    return jsonify(response), 200

def get_all_services():
    # Query ke firestore untuk mendapatkan 'all services'
    services_ref = db.collection('services')
    results = services_ref.stream()

    # Respon
    list_services = []
    for result in results:
        service_info = result.to_dict()
        list_services.append(service_info)

    response = {"list-services": list_services}
    return jsonify(response), 200

def verify_login_admin():
    # Periksa apakah permintaan POST "email" dan "password" ada
    if request.method == 'POST' and 'admin_name' in request.get_json() and 'password' in request.get_json():
        # variabel untuk mendapatkan data dari formulir
        data = request.get_json()
        admin_name = data.get('admin_name')
        plain_password = data.get('password')

        # referensi ke koleksi "user" di Firestore
        accounts_ref = db.collection('admin')

        # Query ke Firestore untuk mencari akun dengan admin_name yang sesuai
        query = accounts_ref.where('admin_name', '==', admin_name)
        results = query.stream()

        # Jika ada akun dengan email yang sesuai
        for result in results:
            account_data = result.to_dict()
            hashed_password = account_data.get("password", "")

            # Periksa apakah plain_password sesuai dengan hashed_password
            if bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8')):
                
                # Generate token baru untuk user
                admin_id = account_data['admin_id']
                admin_name = account_data['admin_name']
                is_admin = account_data['is_admin']
                new_token = generate_token_admin(admin_id, admin_name)

                # Update admin's token di database
                admin_ref = db.collection('admin').document(admin_id)
                admin_ref.update({
                    'token': new_token
                })

                # Retrieve data user yang sudah di update
                updated_admin_data = admin_ref.get().to_dict()

                # variabel data store dan user di firestore untuk response
                token = updated_admin_data.get("token", None)

                # Persiapkan response
                response = {
                    "admin_id": admin_id,
                    "admin_name": admin_name,
                    "token": token,
                    "is_admin" : is_admin
                }

                return jsonify(response), 201

        # Jika akun tidak ditemukan atau password salah
        response = {"error": "Incorrect admin_name/password"}
        return jsonify(response), 401

    # Jika email atau password tidak disertakan dalam permintaan
    response = {"error": "Missing admin_name or password in the request"}
    return jsonify(response), 400


def register_admin():
    
    #user request body
    data = request.get_json()
    admin_name = data.get('admin_name')
    plain_password = data.get('password')

    # generate id admin dengan uuid
    admin_id = str(uuid4())

    # Hash kata sandi menggunakan bcrypt
    hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())

    # Query ke Firestore untuk memeriksa apakah email sudah terdaftar
    nama_exists_query = db.collection('admin').where('admin_name', '==', admin_name)
    nama_exists_result = nama_exists_query.stream()
    # Jika nama sudah terdaftar, kembalikan respons dengan error message
    if len(list(nama_exists_result)) > 0:
        response = {"error": "Admin sudah terdaftar"}
        return jsonify(response), 400
    
    
    # Simpan informasi admin ke Firestore
    admin_ref = db.collection('admin').document(str(admin_id))
    token = generate_token_admin(admin_id, admin_name)
    admin_firestore_data = {
        'created_at': datetime.now(),
        'admin_name':admin_name,
        'admin_id': admin_id,
        'password': hashed_password.decode('utf-8'), 
        'token': token,
        'is_admin': True  
    }
    admin_ref.set(admin_firestore_data)

    # Exclude key 'password dan created at' untuk response
    response_data = {
        key: value for key, value in admin_firestore_data.items() if key not in ['password', 'created_at']
    }
    # Persiapkan response
    response = response_data  

    return jsonify(response), 201  # Mengembalikan respons JSON

def get_consult_service():
    consultation_service_ref = db.collection('consultation_service')
    documents = consultation_service_ref.stream()

    result = []
    for doc in documents:
        document_data = doc.to_dict()
        service_id ={'service_id': document_data.get('service_id', '')}
        result.append(service_id)

    return jsonify(result), 201

def get_messages(service_id):
    message_ref = db.collection('consultation_service').document(service_id).collections()

    chat_collection = []
    for collection in message_ref:
        chat_collection.append({
            'collection_id': collection.id,
        })

    return jsonify(chat_collection), 200