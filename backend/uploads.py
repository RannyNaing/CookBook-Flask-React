import os
from flask import Flask, request, session, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS

UPLOAD_FOLDER = './files/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app, expose_headers='Authorization')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def file_upload():
    target = os.path.join(app.config['UPLOAD_FOLDER'], 'test_docs')
    if not os.path.isdir(target):
        os.mkdir(target)
    
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        destination = os.path.join(target, filename)
        file.save(destination)
        session['uploadFilePath'] = destination
        return jsonify({'file': filename}), 200
    else:
        return jsonify({'error': 'Invalid file type'}), 400

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True, host="0.0.0.0", use_reloader=False)
