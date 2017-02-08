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
    t = Tweet.query.get(id)
    form = request.get_json()
    t.comments_count = int(form['comments_count']) + 1
    del form['comments_count']
    c = Comment(form)
    c.tweet = t
    c.user = u
    c.save()
    t.save()
    c.comments_count = t.comments_count
    print('count',c.comments_count)
    r = {
        'success': True,
        'data': c.json(),
    }
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
    form['transmit'] =id
    bt = Tweet.query.get(id)
    bt.transmit_count = form['transmit_count']
    t = Tweet(form)
    t.user = u
    t.save()
    bt.save()
    t.json()
    t.nickname = u.nickname
    t.portrait = u.portrait
    tweet = Tweet.query.get(id)
    tuser = User.query.filter_by(id=tweet.user_id).first()
    tweet.nickname = tuser.nickname
    r = {
        'success': True,
        'data': t.json(),
        'tweet': tweet.json(),
        'user_id': u.id,
    }
    return jsonify(r)

# 加载微博
@main.route('/loads/<page_id>')
def tweet_loads(page_id):
    u = current_user()
    limit = 12
    if page_id == '1':
        ts = timeline_tweets(u,limit)
    elif page_id == '2':
        ts = plaza_tweets(limit)
    ts = add_userinfo(ts)
    r = dict(
        success=True,
        data=[t.json() for t in ts],
        user_id = u.id,
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
def timeline_tweets(u,limit):
    if u.guanzhu == [] or u.guanzhu is None:
        ts = u.tweets
    else:
        u.format_data()
        guanzhu_id = u.guanzhu
        gid = [ int(x) for x in guanzhu_id if x != '']
        guanzhu_tweets = Tweet.query.filter(Tweet.user_id.in_(gid)).all()
        tweets = u.tweets + guanzhu_tweets
        ts_count = len(tweets)
        if ts_count > limit:
            n = next(n for n in range(limit, ts_count + 1, limit))
        else:
            n = limit
        gid = []
        for t in tweets:
            gid.append(t.id)
        ts = Tweet.query.filter(Tweet.id.in_(gid)).order_by('created_time DESC').limit(n).offset(limit).all()
    return ts


# 加载广场的微博
def plaza_tweets(limit):
    ts_count = Tweet.query.count()
    if ts_count > limit:
        n = next(n for n in range(limit, ts_count + 1, limit))
    else:
        n = limit
    ts = Tweet.query.order_by('created_time DESC').limit(n).offset(limit).all()
    return ts

