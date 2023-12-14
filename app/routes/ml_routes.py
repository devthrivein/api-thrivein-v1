from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.ml_controller import predict

ml_routes = Blueprint('ml_routes', __name__)

@ml_routes.route('/predict', methods=['POST'])
@jwt_required()
def trigger_ml_route():
    return predict()

