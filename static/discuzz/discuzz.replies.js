
var csrf_comment = document.querySelector('.csrf-comment').innerHTML;
var csrf_like = document.querySelector('.csrf-like').innerHTML;
var csrf_dislike = document.querySelector('.csrf-dislike').innerHTML;
const profile_pic = document.querySelector('.profile-pic-url').innerHTML;

var reply_form = $('#discuzz_form');
const all_replies_div = document.querySelector('#all_replies');
var discussion_code = document.querySelector('.code').innerHTML;


// var email = $('#uid');
var reply = $('#reply');
// const all_mails_div = document.querySelector('.all_mails');

var loc = window.location;
var wSStart = 'ws://'
if (loc.protocol === 'https:') {
    wSStart = 'wss://';
}

var endPoint = wSStart + loc.host + loc.pathname;
const endpoint_two = wSStart + loc.host + '/myadmin/';
console.log(endPoint, endpoint_two)

var socket = new ReconnectingWebSocket(endPoint);
// var socket_myadmin = new ReconnectingWebSocket(endpoint_two);

const displayEl = document.querySelector('.participants');

function displayParticipant(person) {
    var person = `
                <ion-chip color="success" onclick="view(this)">
                    <ion-avatar>
                        <img src="${person.profile_pic}">
                    </ion-avatar>
                    <ion-label>
                        ${person.username}
                    </ion-label>
                </ion-chip>
            `;
        displayEl.insertAdjacentHTML('beforeEnd', person);
}
function handleParticipants(part){
    const childNo = displayEl.childElementCount;
    if (childNo === part.length) {
        console.log(`EQUAL ${childNo} === ${part.length}`)
         return;
     }
     else if (childNo < part.length) {
       var start = childNo;
        var end = part.length;
        var participants_to_display = part.slice(start, end);
        for (var i = 0; i < participants_to_display.length; i++) {
            displayParticipant(participants_to_display[i]);
        }
        return;
     }
}

socket.onmessage = (e) => {
    var cleaned_data = JSON.parse(e.data);
    var part = cleaned_data.participants;
    if (cleaned_data.type === 'join') {
        // const incomingtone = new Audio('../../../static/incomingreply.wav');
        // incomingtone.play();
        async function presentToast() {
            const toast = document.createElement('ion-toast');
            toast.message = `${cleaned_data.username} joined the group`;
            toast.color = 'success';
            toast.duration = 3000;

            document.body.appendChild(toast);
            return toast.present();
        }
        presentToast();
    }
    else if (cleaned_data.type === 'reply') {
        const incomingtone = new Audio('../../../static/incomingreply.wav');
        incomingtone.play();
        reply_renderer(cleaned_data);
        console.log('POSTED WELL')
    } else if (cleaned_data.type === 'comment') {
        const incomingtone = new Audio('../../../static/incoming1.wav');
        incomingtone.play();
        comment_renderer(cleaned_data);
    } else if (cleaned_data.type === 'like') {
        const incomingtone = new Audio('../../../static/incoming2.wav');
        incomingtone.play();
        like_renderer(cleaned_data);
    } else if (cleaned_data.type === 'dislike') {
        const incomingtone = new Audio('../../../static/incoming3.wav');
        incomingtone.play();
        dislike_renderer(cleaned_data);
    }

    setTimeout(() => {
        handleComments();
        handleLikes();
        handleDislikes();
    }, 200);
    handleParticipants(part);
}

/* socket_myadmin.onopen = (e) => {
console.log('OPENNDED', e)
} */


socket.onopen = (e) => {
    console.log('OPEN', e);

    var sendJoin = JSON.stringify({
        'type': 'join'
    });

    socket.send(sendJoin);

    handleComments();
    handleLikes();
    handleDislikes();

    reply_form.submit((event) => {
        event.preventDefault();
        var msg = reply.val();

        // Serialized form
        // var formSerialized = form.serialize();

        var sendReply = JSON.stringify({
            'discussion_code': discussion_code,
            'profile_pic': profile_pic,
            'reply': msg,
            'type': 'reply'
        });

        if (msg === '' || msg === 'None') {
            return;
        } else {
            socket.send(sendReply);
            /*  setTimeout(() => {
                socket_myadmin.send(sendReply);
            }, 500); */
        }
        reply.val('');
    });


}
socket.onerror = (e) => {
    console.log('ERROR', e)
    async function presentToast() {
            const toast = document.createElement('ion-toast');
            toast.message = `<strong> Connection lost </strong>`;
            toast.color = 'danger';
            toast.duration = 3000;

            document.body.appendChild(toast);
            return toast.present();
        }
        presentToast();
}
socket.onclose = (e) => {
    console.log('CLOSE', e)
    async function presentToast() {
            const toast = document.createElement('ion-toast');
            toast.message = `<strong> Connection closed </strong>`;
            toast.color = 'warning';
            toast.duration = 3000;

            document.body.appendChild(toast);
            return toast.present();
        }
        presentToast();

}

function handleComments() {
    const comForms = document.querySelectorAll('.commentform');
    comForms.forEach((form, current) => {
        form.addEventListener('submit', (event) => {
            event.preventDefault();
            console.log(current);
            const ID = form.id.split('-')[1];
            const comment_field_value = event.target[1].value;
//            console.log('THE FORM IS: ', comment_field_value, ID);
            const sendComment = JSON.stringify({
                'comment': comment_field_value,
                'profile_pic': profile_pic,
                'id': ID,
                'type': 'comment'
            });
            if (comment_field_value === '') {
                return;
            } else {
                socket.send(sendComment);
                /* setTimeout(() => {
                socket_myadmin.send(sendComment);
                }, 500); */
            }
            event.target[1].value = '';
        });
    });
}

function handleLikes() {
    var likeForms = document.querySelectorAll('.likeform');

    likeForms.forEach((form) => {
        var counter = 1;
        form.addEventListener('submit', (event) => {
            console.log(counter)
            event.preventDefault();
            var ID = form.id.split('-')[1];
            console.log('THE LIKE FORM IS : ', ID);
            var addOrRemoveLike = JSON.stringify({
                'id': ID,
                'type': 'like'
            });
            if (counter === 1 && ID !== 'x') {
                socket.send(addOrRemoveLike);
                /* setTimeout(() => {
                socket_myadmin.send(addOrRemoveLike);
                }, 500); */
                event.stopImmediatePropagation();
                ID = 'x';
                counter = null;
                return false;
            } else {
                return;
            }

        });
    });
}

function handleDislikes() {
    const disLikeForms = document.querySelectorAll('.dislikeform');

    disLikeForms.forEach((form) => {
        var counter = 1;
        form.addEventListener('submit', (event) => {
            event.preventDefault();
            var ID = form.id.split('-')[1];
            var addOrRemoveDisLike = JSON.stringify({
                'id': ID,
                'type': 'dislike'
            });
            if (counter === 1 && ID !== 'x') {
                socket.send(addOrRemoveDisLike);
                /* setTimeout(() => {
                socket_myadmin.send(addOrRemoveLike);
                }, 500); */
                event.stopImmediatePropagation();
                ID = 'x';
                counter = null;
                return false;
            } else {
                return;
            }

        });
    });
}

function reply_renderer(reply_obj) {
    var reply_text = reply_obj.reply;
    var new_reply_txt = reply_text.replace(/\</g, '&lt;');
    var new_reply_txt1 = new_reply_txt.replace(/\>/g, '&gt;');

    const new_reply = `
                <div id="shadow-card-replies">
                    <div>
                        <ion-chip onclick="view(this)" color="primary">
                            <ion-avatar>
                                <img src="${reply_obj.profile_pic}">
                            </ion-avatar>
                            <ion-label>
                                ${ reply_obj.username}
                            </ion-label>
                        </ion-chip>
                        <ion-chip color="primary">
                            <ion-icon name="timer"></ion-icon>
                                <ion-label>
                                0 minutes
                            </ion-label>
                        </ion-chip>
                    </div>
                    <div id="${reply_obj.id}">
<pre id="pre"> 
<code class="prettyprint">
${new_reply_txt1}
</code>
</pre>
                    </div>
                    <div id="options-menu">

                        <form class="likeform" id="like-${reply_obj.id}" method="POST" action="/api/like/${reply_obj.id}/" data-likes="${reply_obj.likes}">
                            ${csrf_like}
                            <button type="submit" class="btn btn-primary bg-primary" name="like" value="${reply_obj.id}">
                            <span class='likess-${reply_obj.id} text-light'><i class="fa fa-thumbs-up">  </i>Likes ${reply_obj.likes}</span>
                            </button>
                        </form>

                        <form class="dislikeform" id="dislike-${reply_obj.id}" method="POST" action="/api/dislike/${reply_obj.id}/">
                            ${csrf_dislike}
                            <button type="submit" class="btn btn-warning bg-warning" name="dislike" value="${reply_obj.id}">
                            <span class='dislikess-${reply_obj.id} text-light'><i class="fa fa-thumbs-down"> </i>Dislikes ${reply_obj.dislikes}</span>
                                </button>
                        </form>

                    </div>

                    <div class="row">
                        <div class="col-md-3 col-sm-12"></div>
                        <div class="col-md-6 col-sm-12">
                            <ion-card class="comments-${reply_obj.id}" color="dark">
                                <h5 class="text-center">Comments</h5>
                                    
                            </ion-card>
                            <div>
                                <div class="form">
                                    <div class="login-form">
                                        <form class="commentform" id="comment-${reply_obj.id}" action="/comments/${reply_obj.id}/" method="POST">
                                            ${csrf_comment}
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
                    <div class="row">
                            <div class="col">
                                <ion-button onclick="showEmojis(this)" class="emoji-show" expand="block"
                                    fill="outline">
                                    <ion-chip>
                                        &#128512;
                                    </ion-chip>
                                    <ion-label> Show emojis </ion-label>
                                </ion-button>
                            </div>
                        <div class="comment-emojis fixed-emoji-div" style="display: none;"></div>
                    </div>

                </div>
            `;

    all_replies_div.insertAdjacentHTML('beforeEnd', new_reply);
    const comment_emojis = document.querySelectorAll('.comment-emojis');
    for (let index = 0; index < comment_emojis.length; index++) {
        CommentEmojis(comment_emojis[index], index)
    }
}

function comment_renderer(comment) {
    const comment_div = document.querySelector(`.comments-${comment.id}`);
    var comm = comment.comment;
    var new_com = comm.replace(/\</g, '&lt;')
    var new_com1 = new_com.replace(/\>/g, '&gt;')
    console.log('the new comm is', comm);
    const comment_to_render = `
                <span class="w-100">
                    <ion-chip onclick="view(this)" color="primary">
                        <ion-avatar>
                             <img src="${comment.profile_pic}">
                        </ion-avatar>
                        <ion-label>
                            ${comment.username}
                        </ion-label>
                    </ion-chip>
                    <ion-chip color="primary">
                        <ion-icon name="timer"></ion-icon>
                        <ion-label>
                            0 minutes
                        </ion-label>
                    </ion-chip>
                </span>
<pre>
<code class="prettyprint">
${new_com1}
</code>
</pre>
<hr class="comment-divider">
            `;
    comment_div.insertAdjacentHTML('beforeEnd', comment_to_render);
}

function like_renderer(like) {
    var like_el = document.querySelector(`.likess-${like.id}`);
    var dislike_el = document.querySelector(`.dislikess-${like.id}`);
    if (like_el === '') {
        return;
    }
    like_el.innerHTML = 'Likes ' + ' ' + like.likes;
    dislike_el.innerHTML = 'Dislikes ' + ' ' + like.dislikes;
}

    function dislike_renderer(like) {
        var dislike_el = document.querySelector(`.dislikess-${like.id}`);
        var like_el = document.querySelector(`.likess-${like.id}`);
        if (dislike_el === '') {
            return;
        }
        dislike_el.innerHTML = 'Dislikes ' + ' ' + like.dislikes;
        like_el.innerHTML = 'Likes ' + ' ' + like.likes;
    }


// for (var i = 0; i < document.forms.length; i++) { document.forms[i].style.display = 'none'; }
