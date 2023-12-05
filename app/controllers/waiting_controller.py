from flask import jsonify
from app.config.config import db

def waiting_list(user_id):
    # set variable is_order_now sebagai false untuk digunakan pada Query
    is_order_now = False

    # Query firestore untuk mendapatkan waiting list order dari user
    list_ref = db.collection('order').where('user_id', '==', user_id).where('is_order_now', '==', is_order_now)
    list_result = list_ref.stream()

    # list untuk menyimpan wating list 
    list_order = []
    for result in list_result:
        list_data = result.to_dict()
        list_data_info = {
            'order_id': list_data.get('order_id'),
            'title': list_data.get('title'),
            'transaction_date': list_data.get('transaction_date')
        }
        list_order.append(list_data_info)

    # Return response
    response = {'waiting_list_order': list_order}
    return jsonify(response), 200


def detail_waiting_order(order_id):
    #query firestore untuk mendapatkan detail waiting list order berdasarkan order_id
    detail_waiting_ref = db.collection('order').document(order_id)
    detail_result = detail_waiting_ref.get().to_dict()

    # Exclude key yang tidak diperlukan
    excluded_fields = ['user_id', 'address', 'consultation_id']

    # return response
    response = {key: value for key, value in detail_result.items() if key not in excluded_fields}
    return jsonify(response), 200
