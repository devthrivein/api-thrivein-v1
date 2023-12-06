from flask import Blueprint
from app.controllers.solutions_controller import (
    list_services, 
    service_detail, 
    service_portfolio, 
    send_order, 
    get_order, 
    order_later, 
    update_order,
)
from flask_jwt_extended import jwt_required

solutions_route = Blueprint('solutions_routes', __name__)

@solutions_route.route('/list-services/<id>', methods=['GET'])
@jwt_required()
def list_services_route(id):
    return list_services(id)

@solutions_route.route('/detail-services/<service_id>', methods=['GET'])
@jwt_required()
def service_detail_route(service_id):
    return service_detail(service_id)

@solutions_route.route('/list-services/<service_id>/portfolio', methods=['GET'])
@jwt_required()
def portfolio_route(service_id):
    return service_portfolio(service_id)

@solutions_route.route('/list-services/order', methods=['POST'])
@jwt_required()
def send_order_route():
    return send_order()

@solutions_route.route('/list-services/order-update/<order_id>', methods=['PUT'])
@jwt_required()
def update_order_route(order_id):
    return update_order(order_id)


@solutions_route.route('/list-services/order-later', methods=['POST'])
@jwt_required()
def order_later_route():
    return order_later()

@solutions_route.route('/list-services/order/<order_id>', methods=['GET'])
@jwt_required()
def get_order_route(order_id):
    return get_order(order_id)