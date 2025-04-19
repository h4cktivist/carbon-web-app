import os

from flask import current_app
from werkzeug.datastructures import FileStorage

import llama_index
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, load_index_from_storage, Settings

import uuid


session_indices = {}


def allowed_file(filename: str):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def save_file(file: FileStorage) -> str:
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    return file.filename


def create_session_id():
    return str(uuid.uuid4())


def load_document_and_create_index(session_id, file_path):
    if session_id in session_indices:
        index = session_indices[session_id]
    else:
        documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
        index = VectorStoreIndex.from_documents(documents)

        session_storage_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], session_id)
        index.storage_context.persist(persist_dir=session_storage_dir)
        session_indices[session_id] = index

    return index


def get_index_for_session(session_id):
    if session_id in session_indices:
        return session_indices[session_id]
    else:
        session_storage_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], session_id)
        if os.path.exists(session_storage_dir):
            print(f"Загружаем индекс с диска для сессии: {session_id}")
            storage_context = StorageContext.from_defaults(persist_dir=session_storage_dir)
            index = load_index_from_storage(storage_context)
            session_indices[session_id] = index
            return index
        else:
            return None


def query_index(session_id, query):
    index = get_index_for_session(session_id)
    if index:
        query_engine = index.as_query_engine()
        response = query_engine.query(query)
        return response
    else:
        return None


def make_response(session_id, request: str, filename=None) -> dict:
    if filename:
        if session_id not in session_indices:
            load_document_and_create_index(session_id,
                                           os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        response = {
            'session_id': session_id,
            'filename': filename,
            'response': query_index(session_id, request).response
        }
    else:
        index = query_index(session_id, request)
        response = {
            'session_id': session_id,
            'filename': filename,
            'response': index.response if index is not None else Settings.llm.complete(request).text
        }
    return response
