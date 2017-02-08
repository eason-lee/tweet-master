/*TMODJS:{"version":7,"md5":"7e724b9997a3db0929da739290ea3339"}*/
template('transmitTweetTemplate',function($data,$filename
/**/) {
'use strict';var $utils=this,$helpers=$utils.$helpers,$escape=$utils.$escape,did=$data.did,dportrait=$data.dportrait,user_id=$data.user_id,dnickname=$data.dnickname,dtime=$data.dtime,dcontent=$data.dcontent,tnickname=$data.tnickname,ttime=$data.ttime,tcontent=$data.tcontent,$each=$utils.$each,timage=$data.timage,value=$data.value,i=$data.i,tid=$data.tid,tpraise=$data.tpraise,ttransmit=$data.ttransmit,tcomments=$data.tcomments,current_user=$data.current_user,dpraise=$data.dpraise,dtransmit_count=$data.dtransmit_count,dcomments_count=$data.dcomments_count,$out='';$out+=' <div id="id-div-tweet-body" class="my-tweet-transmit"> <div class="my-transmit-top"> <div class="modal fade" id="id-div-follow-';
$out+=$escape(did);
$out+='" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="my-modal-follow"> <img src=';
$out+=$escape(dportrait);
$out+=' class="my-portrait-follow img-thumbnail"> <div class="my-follow-button"> <button class="class-button-follow btn btn-primary" data-id="';
$out+=$escape(user_id);
$out+='" data-dismiss="modal" type="button" >关注</button> <button class="class-button-qxfollow btn btn-primary" data-id="';
$out+=$escape(user_id);
$out+='" data-dismiss="modal" type="button" >取消关注</button> </div> </div> </div> <div class="my-tweet-transmit-portrait-1"> <img src=';
$out+=$escape(dportrait);
$out+=' data-id="';
$out+=$escape(did);
$out+='" data-toggle="modal" data-target="#id-div-follow-';
$out+=$escape(did);
$out+='" class="img-portrait"> <h4 class="my-tweet-nickname">';
$out+=$escape(dnickname);
$out+=' <small><footer class="my-tweet-time">微博创建于 <cite title="Source Title">';
$out+=$escape(dtime);
$out+='</cite></footer></small> </h4> </div> <p class="my-tweet-transmit-content"> ';
$out+=$escape(dcontent);
$out+=' <p> </div> <div class="my-transmit-content-tweet"> <div class="my-tweet-transmit-portrait-2"> <h4 class="my-tweet-nickname">';
$out+=$escape(tnickname);
$out+=' <small><footer class="my-tweet-time">微博创建于 <cite title="Source Title">';
$out+=$escape(ttime);
$out+='</cite></footer></small> </h4> </div> <div class="my-transmit-tweet-contents"> <p class=".my-tweet-content"> ';
$out+=$escape(tcontent);
$out+=' <p> <div class="my-tweet-image"> ';
$each(timage,function(value,i){
$out+=' <img src=';
$out+=$escape(value);
$out+=' id=';
$out+=$escape(i);
$out+=' class="my-image"> ';
});
$out+=' </div> </div> <div class="my-tweet-buttons"> <button type="button" class="my-button btn btn-warning"> <span class="glyphicon glyphicon-star-empty"></span> 收藏 </button> <button class=" my-button button btn btn-success" data-id="';
$out+=$escape(tid);
$out+='" value="';
$out+=$escape(tpraise);
$out+='"><span class="glyphicon glyphicon-thumbs-up"></span> ';
$out+=$escape(tpraise);
$out+=' </button> <button class=" my-button button btn btn-info" data-id="';
$out+=$escape(tid);
$out+='" data-target="#myModal"><span class="glyphicon glyphicon-new-window"></span> ';
$out+=$escape(ttransmit);
$out+=' </button> <button class="button-tweet-comment my-button button btn btn-primary" data-id="';
$out+=$escape(tid);
$out+='" data-toggle="collapse" data-target="#collapseExample-';
$out+=$escape(tid);
$out+='" aria-expanded="false" aria-controls="collapseExample"> <span class="glyphicon glyphicon-comment"></span> ';
$out+=$escape(tcomments);
$out+=' </button> </div> </div> ';
if(user_id == current_user ){
$out+=' <div class="my-transmit-bottom-current"> <button class=\'button-tweet-edit my-transmit-button button btn btn-info\' data-id=\'';
$out+=$escape(did);
$out+='\'>编辑</button> <button class=\'button-tweet-delete my-transmit-button button btn btn-danger\' data-id="';
$out+=$escape(did);
$out+='">删除</button> </div> ';
}else{
$out+=' <div class="my-transmit-bottom"> <button type="button" class="my-transmit-button btn btn-warning"> <span class="glyphicon glyphicon-star-empty"></span> 收藏 </button> <button class="button-tweet-praise my-transmit-button button btn btn-success" data-id="';
$out+=$escape(did);
$out+='" value="';
$out+=$escape(dpraise);
$out+='"><span class="glyphicon glyphicon-thumbs-up"></span> ';
$out+=$escape(dpraise);
$out+=' </button> <button id="id-button-transmit-';
$out+=$escape(did);
$out+='" class="button-tweet-transmit my-transmit-button button btn btn-info" data-id="';
$out+=$escape(did);
$out+='" value="';
$out+=$escape(dtransmit_count);
$out+='" data-toggle="modal" data-target="#myModal"> <span class="glyphicon glyphicon-new-window"></span> ';
$out+=$escape(dtransmit_count);
$out+=' </button> <button id="id-button-comment-';
$out+=$escape(did);
$out+='" class="button-tweet-comment my-transmit-button button btn btn-primary" data-id="';
$out+=$escape(did);
$out+='" value="';
$out+=$escape(dcomments_count);
$out+='" data-toggle="collapse" data-target="#collapseExample-';
$out+=$escape(did);
$out+='" aria-expanded="false" aria-controls="collapseExample"><span class="glyphicon glyphicon-comment"> </span> ';
$out+=$escape(dcomments_count);
$out+=' </button> </div> ';
}
$out+=' </div> ';
return new String($out);
});