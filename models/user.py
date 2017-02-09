from . import *
from flask_login import LoginManager
from  werkzeug.security import generate_password_hash
from  werkzeug.security import check_password_hash
from flask_login import UserMixin

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'api.user.login'

class User(ReprMixin, db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    created_time = db.Column(db.Integer, default=timestamp())
    portrait = db.Column(db.String(128), default='')
    nickname = db.Column(db.String(128), default='')
    follow = db.Column(db.Text(128), default='[]')
    followed = db.Column(db.Text(128), default='[]')
    deleted = db.Column(db.Boolean, default=False)
    # 外键关联
    tweets = db.relationship('Tweet', backref='user')
    comments = db.relationship('Comment', backref='user')

    @staticmethod
    def user_by_name(username):
        return User.query.filter_by(username=username).first()

    @classmethod
    def tourist(cls):
        return cls.query.filter_by(id=5).first()

    @property
    def password(self):
        raise AttributeError('不能查看密码')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def add_relation(self,follow_id,form):
        follow = User.query.filter_by(id=follow_id).first()
        gz = form['followed']
        if self.id == follow.id:
            return '不能关注自己'
        if gz == '+1':
            # 添加粉丝
            gz = str(self.id)
            ufollowed = eval(follow.followed)
            if gz not in ufollowed:
                ufollowed.append(gz)
                follow.followed = str(ufollowed)
                follow.save()
            # 添加关注
            fs = str(follow.id)
            ffollow = eval(self.follow)
            if fs not in ffollow:
                ffollow.append(fs)
                self.follow = str(ffollow)
                self.save()
            message = '关注成功'
        elif gz == '-1':
            # 删除粉丝
            fd = str(self.id)
            ufollowed = eval(follow.followed)
            if fd in ufollowed:
                ufollowed.remove(fd)
                follow.followed = str(ufollowed)
                follow.save()
            # 删除关注
            ud = str(follow.id)
            ffollow = eval(self.follow)
            if ud in ffollow:
                ffollow.remove(ud)
                self.follow = str(ffollow)
                self.save()
            message = '已取消关注'
        return message

    def key_mapper(self):
        mapper = {
            'username': 'username',
            'password': 'password',
            'portrait': 'portrait',
            'nickname': 'nickname',
            'followed': 'followed',
            'follow': 'follow',
        }
        return mapper

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def json(self):
        # Model 是延迟载入的, 如果没有引用过数据, 就不会从数据库中加载
        # 引用一下 id 这样数据就从数据库中载入了
        self.id
        self.format_data()
        d = {k: v for k, v in self.__dict__.items() if k not in self.blacklist()}
        print('d', d)
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

    def updates(self, form):
        User.query.filter_by(id=self.id).update(form)
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

    def count_followed(self):
        try:
            followed = len(eval(self.followed))
        except:
            followed = 0
        return followed

    def count_follow(self):
        try:
            follow = len(eval(self.follow))
        except:
            follow = 0
        return follow


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
