from . import *

main = Blueprint('tweet', __name__)

# 添加微博
@main.route('/add', methods=['POST'])
def tweet_add():
    u = current_user()
    form = request.get_json()
    try:
        r = Tweet.add(u,form)
    except:
        r = dict(success=False)
    return jsonify(r)

# 删除微博
@main.route('/delete/<int:id>')
def tweet_delete(id):
    t = Tweet.query.get(id)
    # 获取当前登录的用户, 如果不是这条微博的主人或者管理员, 就返回 401 错误
    user = current_user()
    if user.id != t.user_id and user.id != 1:
        abort(401)
    else:
        try:
            Tweet.delete(id)
            r = {
                'success': True,
                'message': '成功删除',
            }
        except:
            r = dict(success=False)
    return jsonify(r)


# 添加评论
@main.route('/addComment/<int:id>', methods=['POST'])
def tweet_addComment(id):
    u = current_user()
    form = request.get_json()
    try:
        r = Tweet.add_comment(id,u,form)
    except:
        r = dict(success=False)
    return jsonify(r)


# 添加赞
@main.route('/addPraise/<int:id>')
def tweet_addPraise(id):
    u = current_user()
    try:
        r = Tweet.add_praise(id,u)
    except:
        r = dict(success=False)
    return jsonify(r)


# 转发
@main.route('/transmit/<int:id>', methods=['POST'])
def tweet_transmit(id):
    u = current_user()
    form = request.get_json()
    try:
        r = Tweet.add_transmit(id,u,form)
    except:
        r = dict(success=False)
    return jsonify(r)

# 加载plaza微博
@main.route('/loads/plaza/<int:id>')
def tweet_loads_plaza(id):
    u = current_user()
    limit = 12
    if id == 1:
        r = dict(success=False)
    else:
        ts = plaza_tweets(limit,id)
        ts = add_userinfo(ts)
        last_tweet = ts[-1].id
        r = dict(
            success=True,
            data=[t.json() for t in ts],
            user_id = u.id,
            last_tweet=last_tweet,
        )
    return jsonify(r)

# 加载 timeline 微博
@main.route('/loads/timeline/<int:id>')
def tweet_loads_timeline(id):
    u = current_user()
    limit = 12
    if id == 1:
        r = dict(success=False)
    else:
        ts = timeline_tweets(u,limit,id)
        ts = add_userinfo(ts)
        last_tweet = ts[-1].id
        r = dict(
            success=True,
            data=[t.json() for t in ts],
            user_id = u.id,
            last_tweet = last_tweet,
        )
    return jsonify(r)


# 给每条微博加上用户信息
def add_userinfo(ts):
    for t in ts:
        if t.transmit != '0':
            bt = Tweet.query.filter_by(id=int(t.transmit)).first()
            t.tweet = bt.json()
            bu = User.query.filter_by(id=t.user_id).first()
            t.nickname = bu.nickname
            t.portrait = bu.portrait
        else:
            tu = User.query.filter_by(id=t.user_id).first()
            t.nickname = tu.nickname
            t.portrait = tu.portrait
    return ts

# 加载个人主页的微博
def timeline_tweets(u,limit,offset):
    if u.follow == [] or u.follow is None:
        ts = u.tweets
    else:
        u.format_data()
        follow_id = u.follow
        gid = [ int(x) for x in follow_id if x != '']
        follow_tweets = Tweet.query.filter(Tweet.user_id.in_(gid)).all()
        tweets = u.tweets + follow_tweets
        gid = []
        for t in tweets:
            gid.append(t.id)
        ts = Tweet.query.filter(Tweet.id.in_(gid)).order_by('created_time DESC').limit(limit).offset(offset).all()
    return ts


# 加载广场的微博
def plaza_tweets(limit,offset):
    ts = Tweet.query.order_by('created_time DESC').limit(limit).offset(offset).all()
    return ts

