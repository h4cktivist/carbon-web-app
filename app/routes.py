from flask import Blueprint, render_template, request, redirect, url_for, flash

from .utils import allowed_file, save_file, make_response


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/process', methods=['POST'])
def process_request():
    file = request.files['file']

    if file and not allowed_file(file.filename):
        flash('Недопустимый формат файла')
        return redirect(url_for('main.index'))
    else:
        saved_filename = save_file(file)
        response = make_response(saved_filename, request.form['request'])
        return render_template('response.html', response=response)
