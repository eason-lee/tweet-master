var loadTweetsPlaza = function (tweet_id) {
    var success = function (r) {
        if(r.success) {
          loadTemplate(r);
          log('id data ',$('.button-tweet-loadTweets-plaza').data('id'))
          $('.button-tweet-loadTweets-plaza').data('id',r.last_tweet)
        } else {
            alertify.error('没有微博了');
        }
    };
    var error = function(err) {
      log(err);
    };
    vip.loadTweetsPlaza(tweet_id,success,error);
};

var loadTweetsTimeline = function (tweet_id) {
    var success = function (r) {
        if(r.success) {
          loadTemplate(r);
          $('.button-tweet-loadTweets-timeline').data('id',r.last_tweet);
        } else {
            alertify.error('没有微博了');
        }
    };
    var error = function(err) {
      log(err);
    };
    vip.loadTweetsTimeline(tweet_id,success,error);
};

var loadTemplate = function (r) {
    var tweets = r.data;
    var user_id = r.user_id;
    for(var i = 0; i < tweets.length; i++) {
        var t = tweets[i];
        if (t.transmit == '0') {
            var temp = insertTweet(t,user_id);
            if (page == 'plaza'){
                $('.my-connects').append(temp);
            } else {
                $('.my-connect').append(temp);
            }
        } else {
            var data = t;
            var tweet = t.tweet;
            var temp = insertTransmit(data,tweet,user_id);
            if (page == 'plaza'){
                $('.my-connects').append(temp);
            } else {
                $('.my-connect').append(temp);
            }
        }
    }
};
