from flask import Flask, render_template, request, send_from_directory, url_for
import os
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from PIL import Image

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOADED_PHOTOS_DEST'] = UPLOAD_FOLDER

photos = UploadSet('photos', IMAGES) # Images = set of extensions of image files
configure_uploads(app, photos)

app.secret_key = 'This is your secret key to utilize session in Flask'

class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, 'Images only!'),
            FileRequired('File was empty!')
        ]
    )
    submit = SubmitField('Upload')


@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/',  methods=("POST", "GET"))
def uploadFile():
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = url_for('get_file', filename=filename)
    else:
        file_url = None

    return render_template('index.html', form=form, file_url=file_url)

@app.route('/settings',  methods=("POST", "GET"))
def settings():
    print(request.form)
    form = UploadForm()
    file_url = None
    return render_template('index.html', form=form, file_url=file_url)


if __name__ == "__main__":
    app.run(port=3000, debug=True)