// 更新赞
var insertPraise = function(data) {
    log('data',data)
    $('#id-button-praise-' + data.id).find('em').text(data.praise);
};

// 获取赞
var praiseTweet = function(tweet_id) {
    var success = function (r) {
        if(r.success) {
            insertPraise(r.data);
        }
    };
    var error = function(err) {
      log(err);
    };
    vip.tweetAddPraise(tweet_id,success,error);
};
