from flask import jsonify, request
from app.config.config import db

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
    is_order_now = True
    #query firestore untuk mendapatkan detail history order berdasarkan 'order_id'
    order_ref = db.collection('order').where("is_order_now", "==" , is_order_now )
    detail_result = order_ref.stream()

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
    response = {'order_data': all_order}
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