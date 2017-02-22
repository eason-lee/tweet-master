from models import db
from api.file import UPLOAD_FOLDER
from models.user import login_manager
from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
import time
from api.view import  main as view
from api.user import main as user
from api.file import main as file
from api.tweet import main as tweet
# 这里 import 具体的 Model 类是为了给 migrate 用
# 如果不 import 那么无法迁移
# 这是 SQLAlchemy 的机制
from models import User
from models import Tweet
from models import Comment


app = Flask(__name__)
db_path = 'db1.sqlite'
manager = Manager(app)

def register_api(app):
    app.register_blueprint(view)
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(file, url_prefix='/file')
    app.register_blueprint(tweet, url_prefix='/tweet')


def configure_app():
    # 这一行 加了就没 warning
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    # 设置你的加密 key
    app.secret_key = 'secret key'
    # sqlite配置
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path)
    # mysql配置
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://book:book@localhost:3306/tweet'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    # 初始化 db
    db.init_app(app)
    db.app = app
    login_manager.init_app(app)
    # 必须在函数中 import 蓝图
    # 否则循环引用(因为蓝图中 import 了 model, model 引用了这个文件里面目的 db)
    # 注册蓝图
    register_api(app)
    # 注册jinja2的过滤器
    def format_time(btime):
        btime = btime + 28800
        timegm = time.gmtime(btime)
        ftime = time.strftime("%Y-%m-%d  %H:%M:%S", timegm)
        return ftime
    env = app.jinja_env
    env.filters['format_time'] = format_time


def configured_app():
    configure_app()
    return app


# 自定义的命令行命令用来运行服务器
@manager.command
def server():
    print('server run')
    # app = configured_app()
    config = dict(
        debug=True,
        # host='0.0.0.0',
        port=5000,
    )
    app.run(**config)


def configure_manager():
    """
    这个函数用来配置命令行选项
    """
    Migrate(app, db)
    manager.add_command('db', MigrateCommand)

@manager.command
def rebuild_db():
    # 必须初始化 app 才能操作数据库
    db.drop_all()
    db.create_all()
    print('auth rebuild database')

if __name__ == '__main__':
    # configure_manager()
    configure_app()
    # manager.run()
    server()
