from .home import home_controller
from .optimize import optimize_controller
from flask_swagger_ui import get_swaggerui_blueprint

def initControllers(app):
    app.register_blueprint(home_controller)
    app.register_blueprint(optimize_controller)
def register_swagger_ui(app):
    SWAGGER_URL = '/api/swagger'
    API_URL = '/static/swagger_docs/optimization.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Dynamic Image Optimizer API"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)