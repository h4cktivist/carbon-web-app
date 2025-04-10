from flask import Flask
from config import Config
import os


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from .routes import main
    app.register_blueprint(main)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    return app
