from flask import Flask
from flask_cors import CORS
import os
from app.config.config import Config, JWTConfig
from flask_jwt_extended import JWTManager
from app.routes.history_routes import history_routes
from app.routes.home_routes import home_routes
from app.routes.auth_routes import user_routes
from app.routes.solutions_routes import solutions_route
from app.routes.waiting_routes import waiting_routes
from app.routes.user_routes import user_setting_routes
from app.routes.admin_routes import admin_routes
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)

app.config.from_object(Config)

jwt_manager = JWTManager(app)
app.config.from_object(JWTConfig)

#Swagger UI
swagger_url = '/swagger'
api_url = '/static/swagger.json'
swagger_blueprint = get_swaggerui_blueprint(
    swagger_url, 
    api_url,
    config={
        'app_name' : "ThriveIn API"
    }
)

app.register_blueprint(swagger_blueprint, url_prefix = swagger_url)

app.register_blueprint(history_routes)
app.register_blueprint(home_routes)
app.register_blueprint(user_routes)
app.register_blueprint(solutions_route)
app.register_blueprint(waiting_routes)
app.register_blueprint(user_setting_routes)
app.register_blueprint(admin_routes)


if __name__ == '__main__':
    app.run(debug=True, host= "0.0.0.0", port= int(os.environ.get("PORT", 8080)))
