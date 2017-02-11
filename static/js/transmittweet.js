
// 转发微博
var transmitTweet = function() {
    var tweet_id = tweetTransmitId;
    var form = {
        content: $('#id-input-transmit').val(),
    };
    var success = function (r) {
      log('login, ', r);
      if(r.success) {
          var temp = (r.data,r.tweet,r.user_id);
          $('.my-connect').prepend(temp);
          $('#id-button-transmit-' + r.tweet.id).find('em').text(r.tweet.transmit_count);
          $('#id-input-transmit').val("");
          $('#id-button-transmit-off').click();
      } else {
          log('转发失败');
      }
    };
    var error = function (err) {
      log(err);
    };
    vip.transmitTweet(form, tweet_id, success, error);
};

var insertTransmit = function(data,tweet,user_id) {
    var d = data;
    log('data',d);
    var t = tweet;
    var dtime = formatTime(d.created_time);
    var ttime = formatTime(t.created_time);
    if(t.image != '') {
        var timage = t.image;
    } else {
        var timage = t.image;
    }
    var datas = {
        dportrait: d.portrait,
        dcontent: d.content,
        did: d.id,
        user_id: d.user_id,
        dtime: dtime,
        dnickname: d.nickname,
        dpraise: d.praise,
        dcomment: d.comments_count,
        dtransmit: d.transmit_count,
        tcontent: t.content,
        timage: timage,
        tnickname: t.nickname,
        ttime: ttime,
        tid: t.id,
        tpraise: t.praise,
        tcomment: t.comments_count,
        ttransmit: t.transmit_count,
        current_user: user_id,
    };
    log('datas',datas)
    var temp = template('transmitTweetTemplate', datas);
    return temp
}
