from . import *
from .. import login_manager
from  werkzeug.security import generate_password_hash
from  werkzeug.security import check_password_hash
from flask_login import UserMixin



class User(ReprMixin,db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    created_time = db.Column(db.Integer, default=timestamp())
    portrait = db.Column(db.String(128), default='')
    nicheng = db.Column(db.String(128), default='')
    guanzhu = db.Column(db.Text(128), default='[]')
    fans = db.Column(db.Text(128), default='[]')
    # 外键关联
    tweets = db.relationship('Tweet', backref='user')
    comments = db.relationship('Comment', backref='user')

    @staticmethod
    def user_by_name(username):
        return User.query.filter_by(username=username).first()

    def key_mapper(self):
        mapper = {
            'username': 'username',
            'password': 'password',
            'portrait': 'portrait',
            'nicheng': 'nicheng',
            'fans': 'fans',
            'guanzhu': 'guanzhu',
        }
        return mapper

    @property
    def password(self):
        raise AttributeError('不能查看密码')


    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def json(self):
        # Model 是延迟载入的, 如果没有引用过数据, 就不会从数据库中加载
        # 引用一下 id 这样数据就从数据库中载入了
        self.id
        self.format_data()
        d = {k:v for k,v in self.__dict__.items() if k not in self.blacklist()}
        print('d',d)
        return d

    def blacklist(self):
        b = [
            '_sa_instance_state',
            'password',
        ]
        return b


    def validate_auth(self, form):
        username = form.get('username', '')
        password = form.get('password', '')
        username_equals = self.username == username
        password_equals = self.verify_password(password)
        return username_equals and password_equals


    def updates(self,form):
        User.query.filter_by(id = self.id).update(form)
        db.session.commit()

    # 验证注册用户的合法性
    def register_validate(self):
        min_len = 3
        valid_username = User.query.filter_by(username=self.username).first() == None
        valid_username_len = len(self.username) >= min_len
        # valid_password_len = len(self.password) >= min_len
        msgs = []
        if not valid_username:
            message = '用户名已经存在'
            msgs.append(message)
        elif not valid_username_len:
            message = '用户名长度必须大于等于 3'
            msgs.append(message)
        status = valid_username and valid_username_len
        return status, msgs

    def count_fans(self):
        try:
            fans = len(eval(self.fans))
        except:
            fans = 0
        return fans

    def count_guanzhu(self):
        try:
            guanzhu = len(eval(self.guanzhu))
        except:
            guanzhu = 0
        return guanzhu

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))