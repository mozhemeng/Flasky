# -*- coding:utf-8 -*-

from . import auth
from flask import render_template,redirect,request,url_for,flash,abort
from flask_login import login_user, logout_user,login_required,current_user
from ..models import User
from .forms import LoginForm,RegistrationForm,ChangepasswordForm,ResetpasswordRequestForm,\
    ResetpasswordForm,ChangeemailForm
from .. import db
from ..email import send_email


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('用户名或密码错误！')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('注销成功！')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, '验证您的账户','auth/email/confirm', user=user, token=token)
        flash('一封验证邮件已经发送到您的邮箱。')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('您已成功验证邮箱！')
    else:
        flash('验证链接失效，验证失败。')
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, '验证您的账户',
               'auth/email/confirm', user=current_user, token=token)
    flash('一封新的确认邮件已经发送到您的邮箱。')
    return redirect(url_for('main.index'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangepasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            current_user.password = form.nowpassword.data
            db.session.add(current_user)
            db.session.commit()
            logout_user()
            flash('密码修改成功，请使用新密码重新登录！')
            return redirect(url_for('auth.login'))
        else:
            flash('原密码错误，请重试')
    return render_template('auth/change_password.html', form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def reset_password_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = ResetpasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, '重置您的密码',
                       'auth/email/reset_password',
                       user=user, token=token)
        flash('一封重置邮件已经发送到您的邮箱。')
        redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = ResetpasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('邮箱有误，请确认后重新输入。')
            return redirect(url_for('main.index'))
        if user.reset_password(token,form.password.data):
            flash('密码重置成功，请使用新密码登录！')
            return redirect(url_for('auth.login'))
        else:
            flash('邮箱有误，请确认后重新输入。')
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeemailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.newemail.data
            token = current_user.generate_change_email_token(new_email)
            send_email(new_email, '确认您的新邮箱',
                       'auth/email/change_email',
                       user=current_user, token=token)
            flash('一封确认邮件已经发送到您的新邮箱。')
            return redirect(url_for('main.index'))
        else:
            flash('密码或邮箱错误！请重试')
    return render_template('auth/change_email.html', form=form)


@auth.route('/change-email/<token>', methods=['GET', 'POST'])
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash('新邮箱验证成功！')
    else:
        flash('新邮箱验证失败，请重试！')
    return redirect(url_for('main.index'))