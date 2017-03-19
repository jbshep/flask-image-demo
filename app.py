from flask import Flask, render_template, abort, request,\
                    redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

import random
import string
import datetime

app = Flask(__name__)

app.config.from_object('config.DevelopmentConfig')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

IMAGE_DIR = 'static/images'
ERR_NO_FILE_SPECIFIED = 'error: no file specified'


from models import db, Image, add_image, get_image, get_images

db.init_app(app)


def randstr():
    '''Creates a random string of alphanumeric characters.'''
    return ''.join(random.choice(string.ascii_uppercase + string.digits) \
                for _ in range(30))


@app.route('/')
def home():
    return redirect(url_for('show_form'))


@app.route('/images/', methods=['GET'])
def show_form():
    return render_template('form.html')


@app.route('/images/', methods=['POST'])
def upload_image():
    '''Determines where to place the image based on the parameter 'target'.
    Then, we save the image and redirect to GET /images/ with a flash message
    provided.

    The form will have the following parameters.
    target (text): either 'db' or 'file'
    name (text): the name of the image
    file (file): the image's binary data
    '''

    if 'file' not in request.files:
        return ERR_NO_FILE_SPECIFIED

    imgfile = request.files['file']

    if imgfile.filename == '':
        return ERR_NO_FILE_SPECIFIED

    safefilename = secure_filename(randstr() + '-' + imgfile.filename)
    imgpath = '{}/{}'.format(IMAGE_DIR, safefilename)

    target = request.form['target']
    add_image({
        'name': request.form['name'],
        'img_filename' : safefilename if target == 'file' else None,
        'img_data' : imgfile.read() if target == 'db' else None,
    })
    if target == 'file':
        imgfile.save(imgpath)

    flash('New image "{}" created.'.format(request.form['name']))
    return redirect(url_for('show_form'))


@app.route('/images/db/', methods=['GET'])
def get_images_from_db():
    images = get_images()
    images = list(filter(lambda img: img.img_data != None, images))
    return render_template('show_images.html', images=images, target='db')


@app.route('/images/files/', methods=['GET'])
def get_images_from_files():
    images = get_images()
    images = list(filter(lambda img: img.img_filename != None, images))
    return render_template('show_images.html', images=images, target='file')


@app.route('/images/db/<int:the_id>', methods=['GET'])
def get_image_from_db(the_id):
    image = get_image(the_id)
    return app.response_class(image.img_data, mimetype='application/octet-stream')


@app.route('/images/nuke', methods=['GET'])
def nuke_all_images():
    Image.query.delete()
    db.session.commit()
    db.engine.execute('alter sequence images_id_seq RESTART with 1')
    return 'ok'


if __name__ == "__main__":
    app.run()
