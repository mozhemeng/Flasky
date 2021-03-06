# -*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField,BooleanField,SelectField
from wtforms.validators import DataRequired,Length,Email,Regexp
from wtforms import ValidationError
from ..models import User,Role
from flask_pagedown.fields import PageDownField


class NameForm(FlaskForm):
    name = StringField('What is your name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EditProfileForm(FlaskForm):
    name = StringField('真实姓名', validators=[Length(0,64)])
    location = StringField('地址', validators=[Length(0,64)])
    about_me = TextAreaField('简介')
    submit = SubmitField('提交')


class EditProfileAdminForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('用户名', validators=[
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              '用户名只能包含字母、数字、点和下划线')])
    confirmed = BooleanField('是否确认')
    role = SelectField('权限', coerce=int)
    name = StringField('真实姓名', validators=[Length(0,64)])
    location = StringField('地址', validators=[Length(0,64)])
    about_me = TextAreaField('简介')
    submit = SubmitField('提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱地址已注册')

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被占用')


class PostForm(FlaskForm):
    title = StringField("标题", validators=[DataRequired(), Length(max=255)])
    body = TextAreaField("博文", validators=[DataRequired()])
    submit = SubmitField('提交')


class CommentForm(FlaskForm):
    body = PageDownField("评论", validators=[DataRequired()])
    submit = SubmitField('提交')