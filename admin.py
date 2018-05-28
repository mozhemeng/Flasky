from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_login import current_user


class PostModelView(ModelView):
    can_create = False
    column_list = ('id', 'title', 'body', 'author', 'timestamp')
    column_labels = {
        'id': '序号',
        'title': '博文标题',
        'body': '博文内容',
        'author': '博文作者',
        'timestamp': '发布时间'
    }

    def __init__(self, Model, session, **kwargs):
        super(PostModelView, self).__init__(Model, session, **kwargs)

    def is_accessible(self):
        return current_user.is_authenticated and\
            current_user.is_administrator()


class UserModelView(ModelView):
    can_create = False
    column_list = ('id', 'email', 'username', 'confirmed', 'name', 'location',
                   'about_me', 'member_since', 'last_seen', 'role')
    column_labels = {
        'id': '序号',
        'email': '电子邮件',
        'username': '用户名',
        'confirmed': '邮箱验证',
        'name': '姓名',
        'location': '地址',
        'about_me': '简介',
        'member_since': '注册时间',
        'last_seen': '上次登录',
        'role': '用户身份'
    }

    def __init__(self, Model, session, **kwargs):
        super(UserModelView, self).__init__(Model, session, **kwargs)

    def is_accessible(self):
        return current_user.is_authenticated and\
            current_user.is_administrator()


class RoleModelView(ModelView):
    can_create = False
    column_list = ('id', 'name', 'default', 'permissions')
    column_labels = {
        'id': '序号',
        'name': '身份名称',
        'default': '是否默认',
        'permissions': '身份权限'
    }

    def __init__(self, Model, session, **kwargs):
        super(RoleModelView, self).__init__(Model, session, **kwargs)

    def is_accessible(self):
        return current_user.is_authenticated and\
            current_user.is_administrator()


class MyFileAdmin(FileAdmin):
    def is_accessible(self):
        return current_user.is_authenticated and\
            current_user.is_administrator()

