window.onload = (event) => {
    console.log('The event is', event);
    event.preventDefault();
    LoadReplies();
}

const discuzz_form_el = document.querySelector('#discuzz_form');
const all_replies_div = document.querySelector('#all_replies');
const discussion_code = document.querySelector('.code').textContent.split(' ')[1];
const discussion_id = document.querySelector('.code_id').textContent;
const responseDiv = document.querySelector('.response');

function clear_replies() {
    all_replies_div.innerHTML = '';
}

function clear_error() {
    responseDiv.innerHTML = '';
}

const responseDisplay = (parentEl, messsage, type) => {
    const response = `
                <p class="response-msg text-center text-${type}">${messsage}</p>
            `;

    parentEl.insertAdjacentHTML('beforeEnd', response);
};

discuzz_form_el.addEventListener('submit', handleDiscuzzForm);

function handleDiscuzzForm(event) {
    event.preventDefault();
    const myForm = event.target;
    const myFormData = new FormData(myForm);
    const url = myForm.getAttribute('action');
    const method = myForm.getAttribute('method');

    const xhr = new XMLHttpRequest();
    xhr.open(method, url);
    xhr.onload = () => {
        const serverResponse = xhr.response;
        const response_ = JSON.parse(serverResponse);
        clear_replies();
        clear_error();
        LoadReplies();
        myForm.reset();
        responseDisplay(responseDiv, response_.response_msg, response_.response_type);
        setTimeout(() => {
            clear_error();
        }, 1500);
    };
    xhr.send(myFormData);
}

function LoadReplies() {
    var listed_queries = [];

    var page = page;
    var resultsPerPage = resultsPerPage;
    var start = (page - 1) * resultsPerPage;
    var end = page * resultsPerPage;

    const xhr = new XMLHttpRequest();
    const url = `/api/discuzz/${discussion_code}/`;
    const method = "GET";
    const responseType = "json";
    xhr.responseType = responseType;
    xhr.method = method;
    xhr.open(method, url);
    xhr.onload = () => {

        const serverResponse = xhr.response;
        const all_replies_from_server = serverResponse.response;
        // LoadReplies;
        all_replies_from_server.forEach(reply_render);
        // load_Comments();
        const like_form = document.querySelectorAll('.likeform');

        like_form.forEach(element => {
            element.addEventListener('submit', handleLikeForm);
        });

        const dis_like_form = document.querySelectorAll('.dislikeform');

        dis_like_form.forEach(element => {
            element.addEventListener('submit', handleDisLikeForm);
        });

        const comment_form = document.querySelectorAll('.commmentform');

        comment_form.forEach(element => {
            element.addEventListener('submit', handleCommentForm);
        });
        setTimeout(() => {
            load_Comments();
        }, 1500);

    }
    xhr.send();
}

function handleLikeForm(event) {
    event.preventDefault();
    const myForm = event.target;
    const myFormData = new FormData(myForm);
    const id = myForm.getAttribute('id').split('-')[1];

    const url = myForm.getAttribute('action');

    const method = myForm.getAttribute('method');

    const xhr = new XMLHttpRequest();
    xhr.open(method, url);
    xhr.onload = () => {
        const serverResponse = xhr.response;
        const like_btn = document.querySelector(`.likess-${id}`);

        const response_ = JSON.parse(serverResponse);
        const l_u = response_.response;
        var num_likes = parseInt(like_btn.innerHTML);
        if (l_u === 'liked') {
            num_likes++;
        } else if (l_u === 'unliked') {
            num_likes--;
        }
        like_btn.innerHTML = num_likes;

    };
    xhr.send(myFormData);
}

function handleDisLikeForm(event) {
    event.preventDefault();
    const myForm = event.target;
    const myFormData = new FormData(myForm);
    const id = myForm.getAttribute('id').split('-')[1];

    const url = myForm.getAttribute('action');

    const method = myForm.getAttribute('method');

    const xhr = new XMLHttpRequest();
    xhr.open(method, url);
    xhr.onload = () => {
        const serverResponse = xhr.response;
        const dislike_btn = document.querySelector(`.dislikess-${id}`);

        const response_ = JSON.parse(serverResponse);
        const l_u = response_.response;
        var num_dislikes = parseInt(dislike_btn.innerHTML);
        if (l_u === 'disliked') {
            num_dislikes++;
        } else if (l_u === 'undisliked') {
            num_dislikes--;
        }
        dislike_btn.innerHTML = num_dislikes;

    };
    xhr.send(myFormData);
}

function handleCommentForm(event) {
    event.preventDefault();
    const myForm = event.target;

    const myFormData = new FormData(myForm);
    const id = myForm.getAttribute('id').split('-')[1];
    // console.log('THE FORM ID IS', id);

    const url = myForm.getAttribute('action');
    console.log('THE FORM ACTION IS', url);

    const method = myForm.getAttribute('method');

    const xhr = new XMLHttpRequest();
    xhr.open(method, url);
    xhr.onload = () => {
        const serverResponse = xhr.response;
        //const dislike_btn = document.querySelector(`.dislikess-${id}`);

        const response_ = JSON.parse(serverResponse);
        console.log('THE SERVER RESPONSE ON COMMENT TO THIS REPLY IS', response_);
        const comments_div = document.querySelector(`.comments-${id}`);
        const comment_el = `
                    <span class="w-100">${response_.user}</span>
                    <p>${response_.comment}</p>
                `;
        console.log('THE COMMENT DIV IS: ', comments_div);
        comments_div.insertAdjacentHTML('beforeEnd', comment_el);
        myForm.reset();

        // var num_dislikes = parseInt(dislike_btn.innerHTML);
        // if (l_u === 'disliked') {
        //     num_dislikes++;
        // } else if (l_u === 'undisliked') {
        //     num_dislikes--;
        // }
        // dislike_btn.innerHTML = num_dislikes;

    };
    xhr.send(myFormData);
}


function load_Comments() {
    var listed_comments = [];
    console.log('THE CODE IS', discussion_code);
    console.log('THE CODE IS', discussion_id);

    const xhr = new XMLHttpRequest();
    const url = `/comment/?code=${discussion_code}&id=${discussion_id}`;
    const method = "GET";
    const responseType = "json";
    xhr.responseType = responseType;
    xhr.method = method;
    xhr.open(method, url);
    xhr.onload = () => {

        const serverResponse = xhr.response;
        serverResponse.all_comments.forEach(showCommntsAsPerReply);
        console.log('all the comments are as follows', serverResponse.all_comments);
    }
    xhr.send();

}

function showCommntsAsPerReply(comment) {
    console.log('The comment to is', comment.commented_to);
    const comment_el = `
                    <span class="w-100">${comment.commented_by}</span>
                    <p>${comment.comment}</p>
                `;
    const id__ = comment.commented_to;
    const comments_div = document.querySelector(`.comments-${id__}`);

    if (comments_div === null) {
        console.log('COMMENT DIV NOT FOUND')
    } else {
        console.log('This makes the comment div', comments_div);
        comments_div.insertAdjacentHTML('beforeEnd', comment_el);
    }
}


function reply_render(reply_obj) {
    const reply_text = reply_obj.reply;

    const new_reply = `
                <div id="shadow-card-replies">
                    <div>
                        <h6 id="reply-uid"> ${ reply_obj.username} ${reply_obj.id}</h6>
                    </div>
                    <div id="${reply_obj.id}">
<pre id="pre"> 
<code>
${reply_text} 
</code>
</pre>
                    </div>
                    <div id="options-menu">

                        <form class="hide" method="POST" action="{% url 'comment'%}">
                            {% csrf_token %}
                            <button type="submit" name="comment" value="${reply_obj.id}">
                            <i class="fa fa-comment"> <span>${ reply_obj.comments }</span> </i>
                            </button>
                        </form>
                        <form class="likeform" id="like-${reply_obj.id }" method="POST" action="/api/like/${reply_obj.id}/" data-likes="${reply_obj.likes}">
                            {% csrf_token %}
                            <button type="submit" class="btn btn-primary" name="like" value="${reply_obj.id }">
                            <i class="fa fa-thumbs-up"> <span class='likess-${reply_obj.id }'>${reply_obj.likes}</span> </i>
                            </button>
                        </form>

                        <form class="dislikeform" id="dislike-${reply_obj.id }" method="POST" action="/api/dislike/${reply_obj.id}/">
                            {% csrf_token %}
                            <button type="submit" name="dislike" value="${reply_obj.id }">
                            <i class="fa fa-thumbs-down"> <span class='dislikess-${reply_obj.id }' >${reply_obj.dislikes}</span> </i>
                                </button>
                        </form>
                        <form class="shareform" id="share-${reply_obj.id }" class="hide" method="POST" action="">
                            {% csrf_token %}
                            <button disabled="disabled">
                            <i class="fa fa-share"> <span>5</span> </i>
                            </button>
                        </form>

                    </div>

                    <div class="row">
                        <div class="col-md-3 col-sm-12"></div>
                        <div class="col-md-6 col-sm-12">
                            <div class="comments-${reply_obj.id}">
                                
                            </div>
                            <div>
                                <div class="form">
                                    <div class="login-form">
                                        <form class="commmentform" id="comment-${reply_obj.id}" action="/comments/${reply_obj.id}/" method="POST">
                                            {% csrf_token %}
                                            <div class="form-row input">

                                                <div class="form-group col-md-12 inputBox comment-reponse">
                                                    
                                                </div>

                                                <div class="form-group col-md-12 inputBox">
                                                    <label for="reply">Make comment  </label>
                                                    <textarea name="comment" class="inputBox " rows="3" cols="35" placeholder="Make a comment to this reply" required="required"></textarea>
                                                </div>

                                                <div class="form-group col-md-12 inputBox ">
                                                    <button type="submit" name="" class="btn btn-success w-100 ">Comment</button>
                                                </div>

                                            </div>
                                        </form>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3 col-sm-12"></div>
                    </div>


                </div>
            `;
    all_replies_div.insertAdjacentHTML('beforeEnd', new_reply);
}