from . import *

main = Blueprint('view', __name__)


@main.route('/')
def index():
    view = '.login_view'
    return redirect(url_for(view))


# 显示登录界面的函数  GET
@main.route('/login')
def login_view():
    return render_template('login.html')


@main.route('/plaza')
def plaza_view():
    u = current_user()
    u.follow_count = u.count_follow()
    u.followed_count = u.count_followed()
    tweets = Tweet.query.order_by('created_time DESC' ).limit(12).all()
    for t in tweets:
        t.format_data()
        t.comments.sort(key=lambda c: c.created_time, reverse=True)
        t.comments = t.comments[:6]
        if t.transmit == '0':
            t.images = t.image
        else:
            tweet_id = int(t.transmit)
            transmit = Tweet.query.filter_by(id=tweet_id).first()
            if transmit is None:
                transmit = Tweet.query.filter_by(id=9).first()
            else:
                t.transmit_nickname = transmit.user.nickname
            transmit.format_data()
            t.images =transmit.image
            t.tweet = transmit
    return render_template('plaza.html', tweets=tweets,user=u)


@main.route('/timeline')
def user_timeline_view():
    u = current_user()
    if u is None :
        abort(401)
    if u.follow == [] or u.follow is None:
        tweets = u.tweets
    else:
        follow_id = eval(u.follow)
        gid = [ int(x) for x in follow_id if x != '']
        follow_tweets = Tweet.query.filter(Tweet.user_id.in_(gid)).all()
        tweets = u.tweets + follow_tweets
    u.follow_count = u.count_follow()
    u.followed_count = u.count_followed()
    tweets.sort(key=lambda t: t.created_time,reverse=True)
    tweets = tweets[:12]
    for t in tweets:
        t.format_data()
        t.images = t.image
        t.comments.sort(key=lambda c: c.created_time, reverse=True)
        t.comments = t.comments[:6]
        if t.transmit != '0':
            tweet_id = int(t.transmit)
            transmit = Tweet.query.filter_by(id=tweet_id).first()
            if transmit is None:
                transmit = Tweet.query.filter_by(id=9).first()
            else:
                t.transmit_nickname = transmit.user.nickname
            transmit.format_data()
            t.timage = transmit.image
            t.tweet = transmit

    return render_template('timeline.html', tweets=tweets,user=u)

@main.route('/accounts')
def user_accounts_view():
    u = current_user()
    return render_template('accounts.html', user=u)
