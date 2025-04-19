import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
    ALLOWED_EXTENSIONS = set(os.getenv('ALLOWED_EXTENSIONS').split(','))
    LLM_PROVIDER_URL = os.getenv('LLM_PROVIDER_URL')
    LLM_API_KEY = os.getenv('LLM_API_KEY')
    LLM_NAME = os.getenv('LLM_NAME')
