# -*- coding:utf-8 -*-

from flask import Flask, render_template
from config import config
from admin import MyFileAdmin, PostModelView,UserModelView,RoleModelView
from .models import Post, User, Role
from extensions import bootstrap, mail, moment, db, login_manager, pagedown, flask_admin, photos
import os
from flask_uploads import configure_uploads, patch_request_class
import logging


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    flask_admin.init_app(app)
    configure_uploads(app, photos)
    patch_request_class(app)

    flask_admin.add_view(PostModelView(Post, db.session, name='博文管理'))
    flask_admin.add_view(UserModelView(User, db.session, name='用户管理'))
    flask_admin.add_view(RoleModelView(Role, db.session, name='身份管理'))
    path = os.path.join(os.path.dirname(__file__), 'static')
    flask_admin.add_view(MyFileAdmin(path, '/static', name='文件管理'))

    handler = logging.FileHandler('flask_error.log', encoding='UTF-8')
    handler.setLevel(logging.DEBUG)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    from .pic import pic as pic_blueprint
    app.register_blueprint(pic_blueprint, url_prefix='/pic')

    return app