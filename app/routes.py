from flask import Blueprint, render_template, request, session

from .utils import allowed_file, save_file, make_response, create_session_id


main = Blueprint('main', __name__)


@main.route('/')
def index():
    if 'session_id' not in session:
        session['session_id'] = create_session_id()
    return render_template('index.html')


@main.route('/process', methods=['POST'])
def process_request():
    file = request.files['file']

    if file.filename == '':
        response = make_response(session['session_id'], request.form['request'])

    if file and not allowed_file(file.filename):
        return {'error': 'Недопустимый формат файла'}
    else:
        saved_filename = save_file(file)
        response = make_response(session['session_id'], request.form['request'],
                                 filename=saved_filename)
    return render_template('response.html', response=response['response'])
