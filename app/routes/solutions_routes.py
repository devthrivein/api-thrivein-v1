from flask import Blueprint
from app.controllers.solutions_controller import (
    list_services, 
    service_detail, 
    service_portfolio, 
    send_order, 
    get_order, 
    order_later, 
    update_order,
    welcome_message,
    item_service
)
from flask_jwt_extended import jwt_required

solutions_route = Blueprint('solutions_routes', __name__)

@solutions_route.route('/list-services/<category>', methods=['GET'])
@jwt_required()
def list_services_route(category):
    return list_services(category)

@solutions_route.route('/detail-services/<service_id>', methods=['GET'])
@jwt_required()
def service_detail_route(service_id):
    return service_detail(service_id)

@solutions_route.route('/detail-services/<service_id>/portfolio', methods=['GET'])
@jwt_required()
def portfolio_route(service_id):
    return service_portfolio(service_id)

@solutions_route.route('/detail-services/<service_id>/welcome-message', methods=['GET'])
@jwt_required()
def welcome_route(service_id):
    return welcome_message(service_id)

@solutions_route.route('/order-now', methods=['POST'])
@jwt_required()
def send_order_route():
    return send_order()

@solutions_route.route('/order-update/<order_id>', methods=['PUT'])
@jwt_required()
def update_order_route(order_id):
    return update_order(order_id)


@solutions_route.route('/order-later', methods=['POST'])
@jwt_required()
def order_later_route():
    return order_later()

@solutions_route.route('/list-services/order/<order_id>', methods=['GET'])
@jwt_required()
def get_order_route(order_id):
    return get_order(order_id)

@solutions_route.route('/order-packages/<service_id>', methods=['GET'])
@jwt_required()
def get_item_route(service_id):
    return item_service(service_id)