from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.admin_controller import (
    update_status_order, 
    get_all_order, 
    update_banner, 
    get_order_count, 
    get_user_count, 
    admin_get_order, 
    post_article, 
    update_services,
    admin_get_services,
    get_all_services,
    verify_login_admin,
    register_admin)

admin_routes = Blueprint('admin_routes', __name__)

@admin_routes.route('/registerAdmin', methods=['POST'])
def register_route():
    return register_admin()

@admin_routes.route('/loginAdmin', methods=['GET', 'POST'])
def login_route():
    return verify_login_admin()

@admin_routes.route('/order-progress/<order_id>', methods=['PUT'])
@jwt_required()
def update_status_route(order_id):
    return update_status_order(order_id)

@admin_routes.route('/order', methods=['GET'])
@jwt_required()
def all_order_route():
    return get_all_order()

@admin_routes.route('/order/<order_id>', methods=['GET'])
@jwt_required()
def detail_order_route(order_id):
    return admin_get_order(order_id)

@admin_routes.route('/banners/<id>', methods=['PUT'])
@jwt_required()
def update_banner_route(id):
    return update_banner(id)

@admin_routes.route('/order-count', methods=['GET'])
@jwt_required()
def order_count_route():
    return get_order_count()

@admin_routes.route('/user-count', methods=['GET'])
@jwt_required()
def user_count_route():
    return get_user_count()

@admin_routes.route('/post-article', methods=['POST'])
@jwt_required()
def post_article_route():
    return post_article()

@admin_routes.route('/service/<service_id>', methods=['PUT'])
@jwt_required()
def update_service_route(service_id):
    return update_services(service_id)

@admin_routes.route('/getservice/all', methods=['GET'])
@jwt_required()
def get_all_service_route():
    return get_all_services()

@admin_routes.route('/getservice/<service_id>', methods=['GET'])
@jwt_required()
def get_service_route(service_id):
    return admin_get_services(service_id)