from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from flask_pagedown import PageDown
from flask_admin import Admin,AdminIndexView
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class


bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
mail = Mail()
pagedown = PageDown()
flask_admin = Admin(name='Flasky后台管理', index_view=AdminIndexView(
    name='首页', template='admin/index.html', url='/admin'))
login_manager = LoginManager()
login_manager.session_protection = 'strong'   #可设为None,'basic','strong'以提供不同安全等级
login_manager.login_view = 'auth.login'   #设定登录页面的端点
photos = UploadSet('photos', IMAGES)
