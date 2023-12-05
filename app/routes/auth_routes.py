from flask import Blueprint
from app.controllers.auth_controller import register, verify_login

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/register', methods=['POST'])
def register_route():
    return register()

@user_routes.route('/login', methods=['GET', 'POST'])
def login_route():
    return verify_login()