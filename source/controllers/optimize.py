from flask import Blueprint,abort,request
from utils.user_agent import get_user_agent,detect_device
from classes.optimizer import Optimizer

optimize_controller = Blueprint('optimize',__name__)

@optimize_controller.route('/optimize',methods=['GET'])
def optimize_image():
    url = request.args.get('url')
    if not url:
        abort(400, description="Missing 'url' query parameter")
    if not url.startswith(('http://', 'https://')):
        abort(400, description="Invalid URL")
    try:
        client_width = int(request.args.get('width', 0))
        client_height = int(request.args.get('height', 0))
        dpr = float(request.args.get('dpr', 1.0))
    except ValueError:
        abort(400, description="Invalid 'width', 'height', or 'dpr' values (must be numbers)")
    
    accept = request.accept_mimetypes or '*/*'

    user_agent = get_user_agent(request)
    device_type = detect_device(user_agent)
    optimizer = Optimizer(url, device_type)
    optimizer.set_client_dimensions(client_width, client_height)
    optimizer.set_accept_header(accept)
    optimizer.set_dpr(dpr)
    
    return optimizer.optimize()


    