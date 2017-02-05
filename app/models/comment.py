from . import *



class Comment(ReprMixin, db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(128))
    created_time = db.Column(db.Integer, default=0)
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweets.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def key_mapper(self):
        mapper = {
            'comment': 'comment',
        }
        return mapper

    def json(self):
        extra = dict(
            tweet_id=self.tweet_id,
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

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
