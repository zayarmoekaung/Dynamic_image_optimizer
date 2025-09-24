from flask import Flask

from config import Config
from controllers import initControllers,register_swagger_ui
from error_handlers import register_error_handlers
app = Flask(__name__)
app.config.from_object(Config)

initControllers(app)
register_swagger_ui(app)
register_error_handlers(app)

if __name__=='__main__':
    app.run(debug=True)

