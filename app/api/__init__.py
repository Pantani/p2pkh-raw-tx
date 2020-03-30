import logging

from flask import Flask
from flask_bcrypt import Bcrypt
from .config import ProductionConfig

log = logging.getLogger(__name__)
flask_bcrypt = Bcrypt()


def start_app():
    """
    Start flask application in production mode.
    """
    app = Flask(__name__)
    app.config.from_object(ProductionConfig)
    log.info(f'Starting application at port {ProductionConfig.PORT}')
    flask_bcrypt.init_app(app)
    return app
