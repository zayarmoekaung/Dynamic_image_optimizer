from flask import Blueprint,jsonify
from utils.cache import is_avaiable
from flask import request, render_template
home_controller = Blueprint('home',__name__)

@home_controller.route('/')
def index():
    if request.accept_mimetypes.best == 'application/json':
        return jsonify({"message": "Dynamic Image Optimizer", "swagger_url": "/api/swagger"}), 200
    return render_template('index.html')

@home_controller.route('/health')
def health_check():
    try:
        if not is_avaiable():
            return jsonify({"status": "unhealthy", "error": "Cache service is unavailable. Please check your cache configuration or connection."}), 500
        return jsonify({"status": "healthy"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500
