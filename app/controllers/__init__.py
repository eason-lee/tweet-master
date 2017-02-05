from flask import render_template
from flask import Blueprint
from flask import abort

from sqlalchemy import and_
from ..models import User
from ..models import Tweet
from .. import db
from ..api import current_user

main = Blueprint('controllers', __name__)


@main.route('/plaza')
def plaza_view():
    u = current_user()
    u.guanzhu_count = u.count_guanzhu()
    u.fans_count = u.count_fans()
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
                t.transmit_nicheng = transmit.user.nicheng
            transmit.format_data()
            t.images =transmit.image
            t.tweet = transmit
    return render_template('plaza.html', tweets=tweets,user=u)


@main.route('/timeline')
def user_timeline_view():
    u = current_user()
    if u is None :
        abort(401)
    if u.guanzhu == [] or u.guanzhu is None:
        tweets = u.tweets
    else:
        guanzhu_id = eval(u.guanzhu)
        gid = [ int(x) for x in guanzhu_id if x != '']
        guanzhu_tweets = Tweet.query.filter(Tweet.user_id.in_(gid)).all()
        tweets = u.tweets + guanzhu_tweets
    u.guanzhu_count = u.count_guanzhu()
    u.fans_count = u.count_fans()
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
                t.transmit_nicheng = transmit.user.nicheng
            transmit.format_data()
            t.timage = transmit.image
            t.tweet = transmit

    return render_template('timeline.html', tweets=tweets,user=u)

@main.route('/accounts')
def user_accounts_view():
    u = current_user()
    return render_template('accounts.html', user=u)
