from . import *
import pickle
# 添加微博
@main.route('/tweet/add', methods=['POST'])
def tweet_add():
    u = current_user()
    form = request.get_json()
    print('tweet add ',form)

    if 'image' in form:
        image = form['image']
        form['image'] = str(image)
    t = Tweet(form)
    t.user = u
    t.save()
    t.portrait = u.portrait
    t.nicheng = u.nicheng
    r = dict(
        success=True,
        data=t.json(),
        user_id=u.id,
    )
    return jsonify(r)

# 删除微博
@main.route('/tweet/delete/<int:id>')
def tweet_delete(id):
    t = Tweet.query.get(id)
    if t is None:
        abort(404)
    # 获取当前登录的用户, 如果用户没登录或者用户不是这条微博的主人, 就返回 401 错误
    user = current_user()
    if user is None or user.id != t.user_id:
        abort(401)
    else:
        t.delete()
        r = {
            'success': True,
            'message': '成功删除',
        }
    return jsonify(r)


# 添加评论
@main.route('/tweet/addComment/<int:id>', methods=['POST'])
def tweet_addComment(id):
    u = current_user()
    t = Tweet.query.get(id)
    if t is None:
        abort(404)
    form = request.get_json()
    t.comments_count = form['comments_count']
    del form['comments_count']
    c = Comment(form)
    c.tweet = t
    c.user = u
    c.save()
    t.save()
    r = {
        'success': True,
        'data': c.json(),
    }
    return jsonify(r)


# 添加赞
@main.route('/tweet/addPraise/<int:id>', methods=['POST'])
def tweet_addPraise(id):
    t = Tweet.query.get(id)
    if t is None:
        abort(404)
    form = request.get_json()
    t.praise = form['praise']
    t.save()
    r = dict(
        success=True,
        data=t.json(),
    )
    return jsonify(r)


# 转发
@main.route('/tweet/transmit/<int:id>', methods=['POST'])
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
    t.nicheng = u.nicheng
    t.portrait = u.portrait
    tweet = Tweet.query.get(id)
    tuser = User.query.filter_by(id=tweet.user_id).first()
    tweet.nicheng = tuser.nicheng
    r = {
        'success': True,
        'data': t.json(),
        'tweet': tweet.json(),
        'user_id': u.id,
    }
    return jsonify(r)

# 加载微博
@main.route('/tweet/loads/<page_id>')
def tweet_loads(page_id):
    u = current_user()
    if page_id == '1':
        ts = timeline_tweets(u)
    elif page_id == '2':
        ts = plaza_tweets()
    for t in ts:
        if t.transmit != '0':
            bt = Tweet.query.filter_by(id=int(t.transmit)).first()
            t.tweet = bt.json()
            bu = User.query.filter_by(id=t.user_id).first()
            t.nicheng = bu.nicheng
            t.portrait = bu.portrait
        else:
            tu = User.query.filter_by(id=t.user_id).first()
            t.nicheng = tu.nicheng
            t.portrait = tu.portrait
    r = dict(
        success=True,
        data=[t.json() for t in ts],
        user_id = u.id,
    )
    return jsonify(r)

# 加载个人主页的微博
def timeline_tweets(u):
    if u.guanzhu == [] or u.guanzhu is None:
        ts = u.tweets
    else:
        u.format_data()
        guanzhu_id = u.guanzhu
        gid = [ int(x) for x in guanzhu_id if x != '']
        guanzhu_tweets = Tweet.query.filter(Tweet.user_id.in_(gid)).all()
        tweets = u.tweets + guanzhu_tweets
        ts_count = len(tweets)
        if ts_count > 12:
            n = next(n for n in range(12, ts_count + 1, 12))
        else:
            n = 12
        gid = []
        for t in tweets:
            gid.append(t.id)
        ts = Tweet.query.filter(Tweet.id.in_(gid)).order_by('created_time DESC').limit(n).offset(12).all()
    return ts


# 加载广场的微博
def plaza_tweets():
    ts_count = Tweet.query.count()
    if ts_count > 12:
        n = next(n for n in range(12, ts_count + 1, 12))
    else:
        n = 12
    ts = Tweet.query.order_by('created_time DESC').limit(n).offset(12).all()
    return ts

