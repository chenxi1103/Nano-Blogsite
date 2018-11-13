function followStream() {
    $.get("/grumblr/get-followerStream/")
        .done(function (data) {
            var list = $("#follower");
            list.html('');
              f(data,list);
              $(".commentNow").on("click",function (event) {
                  var post_id = $(event.target).data("post-id");
                    var commentContent = $("#comment-content-"+post_id);
                    $.post("/grumblr/add-comments/"+post_id,{"comment":commentContent.val()})
                        .done(function (data) {
                            if(data!=="Error!"){
                                update_comment(post_id)
                            }
                    });
                    commentContent.val("").focus();
              });
          $(".btn-danger").click(deletePost(event));
        });
}
function deletePost(event) {
    $(".btn-danger").on("click",function (event) {
        $.get("/grumblr/deletePost/" + event.target.id)
            .done(function (data) {
                followStream();
            });
    });
}

function deleteComment(event,post_id){
    $(".alert-danger").on("click", function (event) {
        console.log(event.target.id);
        $.get("/grumblr/deleteComment/" + event.target.id)
            .done(function (data) {
                if(post_id!=="other") {
                    console.log("try to update");
                    update_allComment(post_id);
                }else{
                    console.log("try to 刷新");
                    followStream();
                }
            });
    });
}

function update_allComment(id) {
    $.get("/grumblr/get-comments/" + id)
            .done(function (data) {
                var list = $("#comment-show-" + data.post_id);
                list.html('');
            for (var j = 0; j < data.comments.length; j++) {
                    comment = data.comments[j];
                    var new_comment = $(comment.html);
                    new_comment.data("comment-id", comment.id);
                    list.append(new_comment);
                    $(".alert-danger").click(deleteComment(event,id));
                }
                $(".alert-danger").click(deleteComment(event,"other"));
                 $(".btn-danger").click(deletePost(event));
            })
        .fail(function(r,text,error){
        console.log(text,error);
        return error;
       });
}

function update_comment(id) {
        $.get("/grumblr/get-comments/" + id)
            .done(function (data) {
                var list = $("#comment-show-"+data.post_id);
                comment = data.comments[data.comments.length-1];
                var newComment = $(comment.html);
                newComment.data("comment-id", comment.id);
                list.append(newComment);
                $(".alert-danger").click(deleteComment(event,id));
                $(".btn-danger").click(deletePost(event));
            })
        .fail(function(r,text,error){
        console.log(text,error);
        return error;
       });
}
function f(data,list) {
    for (var i = 0; i < data.posts.length; i++) {
              post = data.posts[i];
              var new_post = $(post.html);
              new_post.data("post-id", post.id);
              list.prepend(new_post);
              $("#comment-button-" + post.id).data("post-id", post.id);
              $.get("/grumblr/get-comments/" + post.id)
                  .then(function (commentList) {
                      var commentShow = $("#comment-show-" + commentList.post_id);
                      commentShow.html('')
                      for (var j = 0; j < commentList.comments.length; j++) {
                          comment = commentList.comments[j];
                          var newComment = $(comment.html);
                          newComment.data("comment-id", comment.id);
                          commentShow.append(newComment);
                          $(".alert-danger").click(deleteComment(event,post.id));
                      }
                  });
          }
}
$(document).ready(function(){
    followStream();
    // CSRF set-up copied from Django docs
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });
});