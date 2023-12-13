from flask import jsonify, request
import uuid
import math
from datetime import datetime
from app.config.config import db
from firebase_admin import firestore
from flask_jwt_extended import get_jwt_identity

def list_services(category):

    # Query ke firestore untuk mendapatkan 'list services' berdasarkan kategori
    services_ref = db.collection('services').where('category', '==', category)
    results = services_ref.stream()

    # Respon
    list_services = []
    for result in results:
        service_info = result.to_dict()
        list_services.append(service_info)

    response = {"list-services": list_services}
    return jsonify(response), 200


def service_detail(service_id):
    # Referensi ke collection services untuk mendapatkan detail services berdasarkan 'service_id'
    service_ref = db.collection('services').document(service_id)

    # mendapatkan snapshot
    service_snapshot = service_ref.get()

    # Mengecek apakah dokumen ditemukan
    if not service_snapshot.exists:
        # Jika dokumen tidak ditemukan, kirim respons error
        response = {'error': 'Service not found'}
        return jsonify(response), 404

    # Jika dokumen ditemukan, ambil data dari dokumen
    service_data = service_snapshot.to_dict()

    # respons JSON 
    response = {
        'service_id': service_id,
        'icon_url': service_data.get('icon_url', ''),
        'title': service_data.get('title', ''),
        'price': service_data.get('price', ''),
        'description': service_data.get('description', '')
    }
    return jsonify(response), 200
    
def service_portfolio(service_id):
    # query parameters untuk pagination
    size = request.args.get('size', type=int)
    page = request.args.get('page', type=int)

    # Query ke Firestore untuk mendapatkan detail layanan berdasarkan ID serta implement pagination
    portfolio_ref = db.collection('portfolio')

    # Query untuk mendapatkan semua data
    all_portfolios = portfolio_ref.where('service_id', '==', service_id).stream()

    # Hitung total data
    total_data = len(list(all_portfolios))

    # Hitung total halaman
    total_pages = math.ceil(total_data / size)

    # Query untuk halaman tertentu
    query = portfolio_ref.where('service_id', '==', service_id).limit(size).offset((page - 1) * size)
    results = query.stream()

    # list untuk menyimpan data portfolio
    portfolio_data = []
    for result in results:
        portfolio_info = result.to_dict()
        portfolio_data.append(portfolio_info)

    # return respons JSON dengan data portfolio
    response = {
        "meta": {
            "total_data": total_data,
            "total_pages": total_pages,
            "current_page": page,
            "data_per_page": size
        },
        "portfolio": portfolio_data
    }

    return jsonify(response), 200

def welcome_message (service_id):
    welcome_message_ref = db.collection('welcome_message').where('service_id', '==', service_id)
    results = welcome_message_ref.stream()

    # list untuk menyimpan data portfolio
    welcome_data = []
    for result in results:
        welcome_info = result.to_dict()
        welcome_data.append(welcome_info)

    # return respons JSON dengan data portfolio
    response = {
        "welcome_message": welcome_data
    }

    return jsonify(response), 200
    
def generate_order_id():
    # mendapatkan 'order_id' terakhir yang terdapat pada firestore
    last_order_ref = db.collection('order').order_by('order_id', direction=firestore.Query.DESCENDING).limit(1)
    last_order = next(last_order_ref.stream(), None)

    # Extract the order_id terakhir
    last_order_id = last_order.to_dict().get('order_id') if last_order else None

    # Generate order_id baru
    if last_order_id:
        order_number = int(last_order_id[2:]) + 1
        new_order_id = f"OR{order_number:04}"
    else:
        new_order_id = "OR0001"

    return new_order_id

def generate_invoice_number():
    # Mendapatkan tanggal saat ini dalam format YYYYMMDD
    current_date = datetime.now().strftime("%Y%m%d")

    # Mendapatkan UUID unik
    unique_id = str(uuid.uuid4().int)[:6]

    # Menggabungkan tanggal dan UUID untuk membuat nomor invoice
    invoice_number = f'INV-{current_date}-{unique_id}'

    return invoice_number

def send_order():
    # Mendapatkan user_id dari JWT
    current_user = get_jwt_identity()

    # Variabel data untuk request json
    data = request.get_json()

    # Request body yang diperlukan 
    consultation_id = data.get('consultation_id')
    service_id = data.get('service_id')
    payment_method = data.get('payment_method')
    total_order = data.get('total_order')
    discount = data.get('discount')
    total_pay = data.get('total_pay')

    # Mengambil data service dari koleksi services
    service_ref = db.collection('services').document(service_id)
    service_data = service_ref.get().to_dict()

    # Memastikan service dengan service_id yang diberikan ada
    if not service_data:
        return jsonify({"error": "Service not found"}), 404

    # Mendapatkan title dari service_data
    title = service_data.get('title')

    # Generate order_id baru
    order_id = generate_order_id()
    # Generate invoice
    no_invoice = generate_invoice_number()

    user_ref = db.collection('user').where("user.user_id", "==", current_user).limit(1)
    
    # Pengecekan kembali apakah user_id benar-benar ada
    user_results = list(user_ref.stream())
    
    if not user_results:
        return jsonify({"error": "User not found"}), 404

    # Extract user_data dari user_results
    user_data = user_results[0].to_dict()
        
    # Check apakah ada store address di user_data 
    if 'store' not in user_data or 'address' not in user_data['store']:
        return jsonify({"error": "Store address not found in user data"}), 500

    address = user_data['store']['address']
    name = user_data['user']['name']

    # Simpan data ke Firestore
    order_ref = db.collection('order').document(order_id)
    order_data = {
        "consultation_id": consultation_id, 
        "order_id": order_id,
        "title": title,  # Gunakan title dari service_data
        "transaction_date": datetime.now(),
        "payment_method": payment_method,
        "total_order" : total_order,
        "discount" : discount,
        "total_pay" : total_pay,
        "is_order_now" : True,
        "address": address,
        "status" : "baru",
        "user_id": current_user,
        "service_id": service_id, 
        "name": name,
        "invoice": no_invoice
    }
    order_ref.set(order_data)

    # Response data dan exclude key yang tidak perlu pada response
    response_data = {
        key: value for key, value in order_data.items() if key not in ['consultation_id', 'is_order_now', 'address']
    }

    return jsonify(response_data), 201

def update_order(order_id):
    
    # request body yang diperlukan
    is_order_now = True

    # Query firestore untuk mendaptkan order dari user berdasarkan order_id
    order_ref_query = db.collection('order').where("order_id", "==", order_id)

    # mendapatkan hasil dari query diatas
    order_results = list(order_ref_query.stream())

    if not order_results:
        return jsonify({"error": "Order not found"}), 404
    
    #generate invoice
    no_invoice = generate_invoice_number()

    # Update document yang bersangkutan
    for order_doc in order_results:
        order_doc_ref = db.collection('order').document(order_doc.id)
        order_data_update = {
            "is_order_now": is_order_now,
            "invoice": no_invoice
        }
        order_doc_ref.update(order_data_update)

    #return response
    response_update = {"message": "Ordered Successfully"}
    return jsonify(response_update), 201


def order_later():
    # Mendapatkan user_id dari JWT
    current_user = get_jwt_identity()

    # Variabel data untuk request JSON
    data = request.get_json()

    # Request body yang diperlukan 
    consultation_id = data.get('consultation_id')
    service_id = data.get('service_id')
    payment_method = data.get('payment_method')
    total_order = data.get('total_order')
    discount = data.get('discount')
    total_pay = data.get('total_pay')

    # Mengambil data service dari koleksi services
    service_ref = db.collection('services').document(service_id)
    service_data = service_ref.get().to_dict()

    # Memastikan service dengan service_id yang diberikan ada
    if not service_data:
        return jsonify({"error": "Service not found"}), 404

    # Mendapatkan title dari service_data
    title = service_data.get('title')

    # Generate a new order_id
    order_id = generate_order_id()

    user_ref = db.collection('user').where("user.user_id", "==", current_user).limit(1)
    
    # Pengecekan kembali apakah user_id ada 
    user_results = list(user_ref.stream())
    
    if not user_results:
        return jsonify({"error": "User not found"}), 404

    # Extract user_data dari user_result
    user_data = user_results[0].to_dict()
    
    # Check apakah ada store address di document yang bersangkutan 
    if 'store' not in user_data or 'address' not in user_data['store']:
        return jsonify({"error": "Store address not found in user data"}), 500

    address = user_data['store']['address']
    name = user_data['user']['name']

    # Simpan order data ke Firestore
    order_ref = db.collection('order').document(order_id)
    order_data = {
        "consultation_id": consultation_id, 
        "order_id": order_id,
        "title": title,
        "transaction_date": datetime.now(),
        "payment_method": payment_method,
        "total_order" : total_order,
        "discount" : discount,
        "total_pay" : total_pay,
        "is_order_now" : False,
        "address": address,
        "status" : "baru",
        "user_id": current_user,
        "service_id": service_id,
        "name": name 
    }
    order_ref.set(order_data)

    # Response data
    response_data = {
        key: value for key, value in order_data.items() if key not in ['consultation_id', 'is_order_now','address']
    }

    # Return response
    return jsonify(response_data), 200

def get_order(order_id): 
    # Query ke firestore untuk mendapatkan data order berdasarkan order_id
    order_ref = db.collection('order').where("order_id","==",order_id)
    order_result = order_ref.get()

    # Check apakah order_id yang dimaksud ada pada firestore
    if order_result:
        # Extract data from the first document in the result
        order_data = order_result[0].to_dict()

        # Prepare the response
        response = order_data

        return jsonify(response), 200
    else:
        # If the order with the specified order_id is not found, return an error response
        error_response = {"error": "Order not found"}
        return jsonify(error_response), 404
    
def item_service(service_id):
    item_ref = db.collection('item_service').where("service_id", "==", service_id)
    results = item_ref.stream()

    # list untuk menyimpan data article 
    item_data = []
    for result in results:
        item_info = result.to_dict()

        # Menghilangkan 'service_id' dari setiap elemen
        item_info.pop('service_id', None)

        item_data.append(item_info)

    # return response
    response = {
        "item": item_data
    }

    return jsonify(response), 200