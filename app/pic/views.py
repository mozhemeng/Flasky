from .forms import PicUpLoadForm
from extensions import photos
from flask import flash, render_template, request, current_app, redirect,url_for
from . import pic
import hashlib
import time
import os


@pic.route('/', methods=['GET', 'POST'])
def upload_file():
    form = PicUpLoadForm()
    if form.validate_on_submit():
        for filename in request.files.getlist('photo'):
            md5 = hashlib.md5()
            md5.update(('admin'+str(time.time())).encode('utf-8'))
            name = md5.hexdigest()[:15]
            photos.save(filename, name=name+'.')
        flash('上传成功！')
    return render_template('pic/index.html', form=form)


@pic.route('/manage')
def manage_file():
    files_list = os.listdir(current_app.config['UPLOADED_PHOTOS_DEST'])
    return render_template('pic/manage.html', files_list=files_list)


@pic.route('/open/<filename>')
def open_file(filename):
    file_url = photos.url(filename)
    return render_template('pic/browser.html', file_url=file_url)


@pic.route('/delete/<filename>')
def delete_file(filename):
    file_path = photos.path(filename)
    os.remove(file_path)
    return redirect(url_for('pic.manage_file'))