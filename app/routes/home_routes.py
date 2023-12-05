from flask import Blueprint
from app.controllers.home_controller import get_banner, services, articles
from flask_jwt_extended import jwt_required

home_routes = Blueprint('home_routes', __name__)

@home_routes.route('/banners', methods=['GET'])
@jwt_required()
def banners_route():
    return get_banner()

@home_routes.route('/articles', methods=['GET'])
@jwt_required()
def articles_route():
    return articles()

@home_routes.route('/services', methods=['GET'])
def services_route():
    return services()