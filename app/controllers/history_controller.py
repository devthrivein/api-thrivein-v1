from flask import jsonify
from app.config.config import db

def history_order(user_id):
    #query firestore untuk mendapatkan history order dari user
    history_ref = db.collection('order').where('user_id', '==', user_id)
    history_results = history_ref.stream()

    #list untuk data 'history_order'
    history_order = []
    for result in history_results:
        history_data = result.to_dict()
        history_order_info = {
            'order_id': history_data.get('order_id'),
            'title': history_data.get('title'),
            'transaction_date': history_data.get('transaction_date')
        }
        history_order.append(history_order_info)
    
    #return response
    response = {'history_order': history_order}
    return jsonify(response), 200

def detail_history_order(order_id):
    #query firestore untuk mendapatkan detail history order berdasarkan 'order_id'
    detail_history_ref = db.collection('order').document(order_id)
    detail_result = detail_history_ref.get().to_dict()

    # Exclude key yang tidak perlu untuk respons
    excluded_fields = ['user_id', 'consultation_id']

    # return response
    response = {key: value for key, value in detail_result.items() if key not in excluded_fields}
    return jsonify(response), 200

