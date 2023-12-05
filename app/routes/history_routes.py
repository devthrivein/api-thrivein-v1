from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.history_controller import history_order, detail_history_order

history_routes = Blueprint('history_routes', __name__)

@history_routes.route('/history-order', methods=['GET'])
@jwt_required()
def history_route():
    user_id = get_jwt_identity()
    return history_order(user_id)

@history_routes.route('/history-order/<order_id>', methods=['GET'])
@jwt_required()
def detail_history_route(order_id):
    return detail_history_order(order_id)