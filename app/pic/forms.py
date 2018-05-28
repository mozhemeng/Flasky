from flask import Flask, render_template
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from extensions import photos


class PicUpLoadForm(FlaskForm):
    photo = FileField('图片文件', validators=[FileAllowed(photos, '只能上传图片！'), FileRequired('文件未选择！')])
    submit = SubmitField('上传')