from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.waiting_controller import waiting_list, detail_waiting_order

waiting_routes = Blueprint('waiting_routes', __name__)

@waiting_routes.route('/waiting-order', methods=['GET'])
@jwt_required()
def waitng_route():
    user_id = get_jwt_identity()
    return waiting_list(user_id)

@waiting_routes.route('/waiting-order/<order_id>', methods=['GET'])
@jwt_required()
def detail_waiting_route(order_id):
    return detail_waiting_order(order_id)