from flask_sqlalchemy import SQLAlchemy
import time


db = SQLAlchemy()

def timestamp():
    return int(time.time())


class ReprMixin(object):
    def __init__(self, json_dict):
        super(ReprMixin, self).__init__()
        self._obj_from_json(json_dict)
        self.created_time = timestamp()

    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ('{0} = {1}'.format(k, v) for k, v in self.__dict__.items())
        return '<{0}: \n  {1}\n>'.format(class_name, '\n  '.join(properties))

    def key_mapper(self):
        """Force subclasses to implement this method"""
        raise NotImplementedError

    def _obj_from_json(self, json_obj):
        """Private method"""
        mapper = self.key_mapper()
        for k, v in mapper.items():
            try:
                paths = v.split('.')
                v = json_obj
                for p in paths:
                    v = v[p]
            except Exception as e:
                v = None
            setattr(self, k, v)

    def formatted_time(self):
        timestamp = float(self.created_time)
        ft = time.ctime(timestamp)
        return ft


    def format_data(self):
        if self.deleted != True:
            for k, v in self.__dict__.items():
                if isinstance(v,str) and len(v) > 2:
                    if '[' == v[0] and ']'== v[-1]:
                        v = eval(v)
                if v == '[]':
                    v = []
                self.__dict__[k] = v


    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete(cls,id):
        data = cls.query.get(id)
        db.session.delete(data)
        db.session.commit()


# 在 ReprMixin 后导入所有 model 类
from .user import User
from .tweet import Tweet
from .comment import Comment
