import os

from flask import current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


def allowed_file(filename: str):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def save_file(file: FileStorage) -> str:
    filename = secure_filename(file.filename)
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    return filename


def process_data_from_file(filename: str) -> str:
    return f'Какие-то данные из {filename}'


def make_response(request: str, filename=None) -> str:
    if filename:
        data = process_data_from_file(filename)
    else:
        data = ''
    return f'Какой-то вывод по запросу {request} на основе {data}'
