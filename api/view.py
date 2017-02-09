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

def format_tweets(tweets):
    ts = []
    for t in tweets:
        if t.deleted != True:
            t.format_data()
            t.comments.sort(key=lambda c: c.created_time, reverse=True)
            t.comments = t.comments[:6]
            t.transmit_count = len(t.transmit_count)
            t.praise = len(t.praise)
            if t.transmit == '0':
                t.images = t.image
            else:
                tweet_id = int(t.transmit)
                transmit = Tweet.query.filter_by(id=tweet_id).first()
                if transmit is None:
                    transmit = Tweet.query.filter_by(id=9).first()
                else:
                    t.transmit_count = len(eval(transmit.transmit_count))
                    t.praise = len(eval(transmit.praise))
                    t.comments_count = transmit.comments_count
                    t.transmit_nickname = transmit.user.nickname
                transmit.format_data()
                t.images = transmit.image
                t.tweet = transmit
            ts.append(t)
    return ts

@main.route('/plaza')
def plaza_view():
    u = current_user()
    u.follow_count = u.count_follow()
    u.followed_count = u.count_followed()
    tweets = Tweet.query.order_by('created_time DESC' ).limit(12).all()
    ts = format_tweets(tweets)
    return render_template('plaza.html', tweets=ts,user=u)


@main.route('/timeline')
def user_timeline_view():
    u = current_user()
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
    ts = format_tweets(tweets)
    return render_template('timeline.html', tweets=ts,user=u)

@main.route('/accounts')
def user_accounts_view():
    u = current_user()
    return render_template('accounts.html', user=u)
