from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.user_controller import logout, update_user, update_store

user_setting_routes = Blueprint('user_setting_routes', __name__)

@user_setting_routes.route('/logout', methods=['POST'])
@jwt_required()
def logout_user_routes():
    return logout()

@user_setting_routes.route('/update-user', methods=['PUT'])
@jwt_required()
def update_user_route():
    return update_user()

@user_setting_routes.route('/update-store', methods=['PUT'])
@jwt_required()
def update_store_route():
    return update_store()