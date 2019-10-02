import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug import secure_filename
from models import callAPI

UPLOAD_FOLDER = './static/images/upload'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.secret_key='flash_key'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('ファイルを選択して下さい')
            return render_template('index.html')

        file = request.files['file']
        if not allowed_file(file.filename):
            flash('拡張子はpng, jpg, jpegのみ使用可能です')
            return render_template('index.html')

        else:
            filename=secure_filename(file.filename)
            file_path=os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            return render_template('display_img.html', file_path=file_path)
    else:
        return render_template('index.html')

@app.route('/classify', methods=['GET', 'POST'])
def classify_img():
    if request.method == 'POST':
        file_path = request.form['image']
        data = callAPI(file_path)

        return render_template('classify_img.html', fish_data=data, file_path=file_path)

    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
