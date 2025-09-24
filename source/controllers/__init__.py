from .home import home_controller
from .optimize import optimize_controller

def initControllers(app):
    app.register_blueprint(home_controller)
    app.register_blueprint(optimize_controller)