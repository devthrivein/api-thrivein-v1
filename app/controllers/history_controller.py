from flask import jsonify
from app.config.config import db

def history_order(user_id):
    # Query firestore to get history order from the user
    history_ref = db.collection('order').where('user_id', '==', user_id)
    history_results = history_ref.stream()

    # List for data 'history_order'
    history_order = []
    for result in history_results:
        history_data = result.to_dict()

        # Get service_id from the order
        service_id = history_data.get('service_id')

        # Query firestore to get service info based on service_id
        service_ref = db.collection('services').document(service_id)
        service_data = service_ref.get().to_dict()

        # Build history_order_info with icon_url from services
        history_order_info = {
            'order_id': history_data.get('order_id'),
            'title': history_data.get('title'),
            'transaction_date': history_data.get('transaction_date'),
            'icon_url': service_data.get('icon_url')
        }
        history_order.append(history_order_info)

    # Return response
    response = {'history_order': history_order}
    return jsonify(response), 200

def detail_history_order(order_id):
    # Query firestore untuk mendapatkan detail history order berdasarkan 'order_id'
    detail_history_ref = db.collection('order').document(order_id)
    detail_result = detail_history_ref.get().to_dict()

    # Mendapatkan service_id dari order
    service_id = detail_result.get('service_id')

    # Query firestore untuk mendapatkan info service berdasarkan service_id
    service_ref = db.collection('services').document(service_id)
    service_data = service_ref.get().to_dict()

    # Memastikan service dengan service_id yang diberikan ada
    if not service_data:
        return jsonify({"error": "Service not found"}), 404

    # Mendapatkan icon_url dari service_data
    icon_url = service_data.get('icon_url')

    # Exclude key yang tidak perlu untuk respons
    excluded_fields = ['is_order_now']

    # Menambahkan icon_url ke respons
    response = {key: value for key, value in detail_result.items() if key not in excluded_fields}
    response['icon_url'] = icon_url

    return jsonify(response), 200


