from flask import Blueprint,jsonify

home_controller = Blueprint('home',__name__)

@home_controller.route('/')
def index():
    return jsonify({"message":"Dynamic Image Optimizer"})