import os
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask

from config import DevelopmentConfig


def add_logs(app):
    if not os.path.exists("logs"):
        os.mkdir("logs")
    file_handler = RotatingFileHandler(
        "logs/avia_flight.log", maxBytes=10240, backupCount=10
    )
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s "
            "[in %(pathname)s:%(lineno)d]"
        )
    )
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info("avia_flight startup")


def create_app():
    app = Flask(__name__)
    config = os.environ.get('APP_SETTINGS') or DevelopmentConfig
    app.config.from_object(config)

    from app.errors.blueprint import bp as errors_bp
    from app.main.blueprint import bp as main_bp

    app.register_blueprint(errors_bp)
    app.register_blueprint(main_bp, url_prefix="/api/v1/")

    if not app.testing:
        add_logs(app)

    return app
