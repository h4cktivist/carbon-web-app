from flask import Flask
from config import Config
import os

from llama_index.core import Settings
from llama_index.llms.nvidia import NVIDIA
from llama_index.embeddings.nvidia import NVIDIAEmbedding


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from .routes import main
    app.register_blueprint(main)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    Settings.embed_model = NVIDIAEmbedding(truncate="END",
                                           api_key=app.config['LLM_API_KEY'])
    Settings.llm = NVIDIA(
        api_key=app.config['LLM_API_KEY'],
        model=app.config['LLM_NAME']
    )

    return app
