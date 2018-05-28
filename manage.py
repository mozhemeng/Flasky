from app import create_app
from extensions import db
from app.models import User, Follow, Role, Permission, Post, Comment, Album, Photo
from flask_migrate import Migrate


app = create_app('development')
migrate = Migrate(app, db)


def setup_db(app, sqla, database=None):
    db_uri, _ = app.config['SQLALCHEMY_DATABASE_URI'].rsplit('/', 1)
    db_name = _.split('?')[0]
    if database:
        db_name = database
    default_engine = sqla.create_engine(db_uri + '/mysql')
    conn = default_engine.connect()
    res = conn.execute('show databases')
    res = [x[0] for x in res]
    if db_name in res:
        print(db_name, 'database existed')
    else:
        conn.execute('commit')
        conn.execute('create database %s character set = utf8mb4' % db_name)
        conn.close()
        print(db_name, 'created')
    # create tables
    sqla.create_all()
    print('tables created')


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, Follow=Follow, Role=Role,
                Permission=Permission, Post=Post, Comment=Comment, Album=Album, Photo=Photo)


@app.cli.command()
def deploy():
    from app.models import Role
    setup_db(app, db)
    Role.insert_roles()


if __name__ == '__main__':
    app.run()