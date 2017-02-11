from . import *
from .comment import Comment

class Tweet(ReprMixin,db.Model):
    __tablename__ = 'tweets'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(128))
    image = db.Column(db.Text(1024), default='')
    created_time = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    praise = db.Column(db.String(1024), default='[]')
    transmit = db.Column(db.String(128), default=0)
    transmit_count = db.Column(db.String(1024), default='[]')
    comments = db.relationship('Comment',backref='tweet')
    comments_count = db.Column(db.Integer,default=0)
    deleted = db.Column(db.Boolean,default=False)

    @classmethod
    def add(cls,user,form):
        if 'image' in form:
            image = form['image']
            form['image'] = str(image)
        t = cls(form)
        t.user = user
        t.praise = '[]'
        t.transmit_count = '[]'
        t.save()
        t.portrait = user.portrait
        t.nickname = user.nickname
        r = dict(
            success=True,
            data=t.json(),
            user_id=user.id,
        )
        return r

    # @classmethod
    # def delete(cls,id):
    #     m = cls.query.get(id)
    #     m.deleted = True
    #     m.save()


    @classmethod
    def add_praise(cls,tweet_id,user):
        t = cls.query.get(tweet_id)
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

    @classmethod
    def add_transmit(cls,tweet_id,user,form):
        u = user
        form['transmit'] = tweet_id
        bt = cls.query.get(tweet_id)
        c = eval(bt.transmit_count)
        if u.id not in c:
            c.append(u.id)
            bt.transmit_count = str(c)
            t = Tweet(form)
            t.user = u
            t.save()
            bt.save()
            t.json()
            t.nickname = u.nickname
            t.portrait = u.portrait
            tuser = User.query.filter_by(id=bt.user_id).first()
            bt.nickname = tuser.nickname
            bt.transmit_count = len(eval(bt.transmit_count))
            r = {
                'success': True,
                'data': t.json(),
                'tweet': bt.json(),
                'user_id': u.id,
            }
        return r

    @classmethod
    def add_comment(cls,tweet_id,user,form):
        t = cls.query.get(tweet_id)
        t.comments_count = int(form['comments_count']) + 1
        del form['comments_count']
        c = Comment(form)
        c.tweet = t
        c.user = user
        c.save()
        t.save()
        c.comments_count = t.comments_count
        r = {
            'success': True,
            'data': c.json(),
        }
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

