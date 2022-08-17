from flask import Flask, render_template, request, session
from imageProcessing import imageProcessing
import os
from werkzeug.utils import secure_filename




app = Flask(__name__)

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = 'This is your secret key to utilize session in Flask'

@app.route('/flask', methods=['GET'])
def index():
    img = "data/letter.png"
    imageProc = imageProcessing(img)
    img = imageProc.run(img)
    print(img)
    return render_template('index.html', user_image = img)

@app.route('/',  methods=("POST", "GET"))
def uploadFile():
    if request.method == 'POST':
        # Upload file flask
        uploaded_img = request.files['uploaded-file']
        # Extracting uploaded data file name
        img_filename = secure_filename(uploaded_img.filename)
        # Upload file to database (defined uploaded folder in static path)
        uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
        # Storing uploaded file path in flask session
        session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)

        return render_template('imageupload.html')
 
    return render_template('index.html')

@app.route('/imageshow')
def displayImage():
    # Retrieving uploaded file path from session
    img_file_path = session.get('uploaded_img_file_path', None)
    # Display image in Flask application web page
    return render_template('index.html', user_image = img_file_path)

if __name__ == "__main__":
    app.run(port=3000, debug=True)