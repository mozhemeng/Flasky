# -*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired,Length,Email,Regexp,EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64),Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('用户名', validators=[
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              '用户名只能包含字母、数字、点和下划线')])
    password = PasswordField('密码', validators=[DataRequired(), EqualTo('password2', message='两次密码必须相同')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱地址已注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被占用')


class ChangepasswordForm(FlaskForm):
    password = PasswordField('原密码', validators=[DataRequired()])
    nowpassword = PasswordField('新密码', validators=[DataRequired()])
    nowpassword2 = PasswordField('确认新密码',
                                 validators=[DataRequired(), EqualTo('nowpassword', message='两次密码必须相同')])
    submit = SubmitField('提交')


class ResetpasswordRequestForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    submit = SubmitField('重置密码')


class ResetpasswordForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('新密码', validators=[DataRequired()])
    password2 = PasswordField('确认新密码', validators=[DataRequired(), EqualTo('password', message='两次密码必须相同')])
    submit = SubmitField('提交')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('该邮箱未注册，请确认后重新输入。')


class ChangeemailForm(FlaskForm):
    newemail = StringField('新邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('提交')

    def validate_newemail(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱地址已注册')