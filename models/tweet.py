from . import *


class Tweet(ReprMixin,db.Model):

    __tablename__ = 'tweets'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(128))
    image = db.Column(db.Text(1024), default='')
    created_time = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    praise = db.Column(db.Integer, default='[]')
    transmit = db.Column(db.String(128), default=0)
    transmit_count = db.Column(db.Integer, default=0)
    comments = db.relationship('Comment',backref='tweet')
    comments_count = db.Column(db.Integer,default=0)

    @classmethod
    def add(cls,user,form):
        if 'image' in form:
            image = form['image']
            form['image'] = str(image)
        t = cls(form)
        t.user = user
        t.save()
        t.portrait = user.portrait
        t.nickname = user.nickname
        r = dict(
            success=True,
            data=t.json(),
            user_id=user.id,
        )
        return r

    @classmethod
    def add_praise(cls,tweet_id,user):
        t = cls.query.filter_by(id=tweet_id).first()
        praise = eval(t.praise)
        if user.id in praise:
            praise.remove(user.id)
        else:
            praise.append(user.id)
        c = len(praise)
        t.praise = str(praise)
        t.save()
        t.praise = c
        r = dict(
            success=True,
            data=t.json(),
        )
        return r

    def key_mapper(self):
        mapper = {
            'content': 'content',
            'image': 'image',
            'praise': 'praise',
            'transmit': 'transmit',
            'transmit_count': 'transmit_count',
            'comments_count': 'comments_count',
        }
        return mapper

    def json(self):
        extra = dict(
            user_id=self.user_id,
        )
        self.format_data()
        d = {k:v for k,v in self.__dict__.items() if k not in self.blacklist()}
        d.update(extra)
        return d

    def blacklist(self):
        b = [
            '_sa_instance_state',
        ]
        return b

