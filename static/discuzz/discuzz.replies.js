
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
//        handleLikes();
//        handleDislikes();
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
//    handleLikes();
//    handleDislikes();

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


function handleMakeComment(event){
    event.preventDefault();
    console.log('THE EVENT IS COMING AGAIN', event)
}



function handleComments() {

    const comForms = document.querySelectorAll('.commentform');
    comForms.forEach((form, current) => {
        form.addEventListener('submit', (event) => {
            event.preventDefault();
            console.log(' THE CURRENT EVENT IS', event);
            const ID = form.id.split('-')[1];
            const comment_field_value = event.target[0].value;
            console.log('THE FORM IS: ', comment_field_value, ID);
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
            }
            event.target[0].value = '';
        });
    });
}


function handleLike(like){
            var ID = like.id.split('-')[1];
            console.log('THE LIKE button IS : ', ID);
            var addOrRemoveLike = JSON.stringify({
                'id': ID,
                'type': 'like'
            });
            var counter = 1;
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
}

function handleDisLike(dislike){
            var ID = dislike.id.split('-')[1];
            console.log('THE DISLIKE button IS : ', ID);
            var addOrRemoveLike = JSON.stringify({
                'id': ID,
                'type': 'dislike'
            });
            var counter = 1;
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
}



//function handleLikes() {
//    var likeForms = document.querySelectorAll('.likeform');
//
//    likeForms.forEach((form) => {
//        var counter = 1;
//        form.addEventListener('submit', (event) => {
//            console.log(counter)
//            event.preventDefault();
//            var ID = form.id.split('-')[1];
//            console.log('THE LIKE FORM IS : ', ID);
//            var addOrRemoveLike = JSON.stringify({
//                'id': ID,
//                'type': 'like'
//            });
//            if (counter === 1 && ID !== 'x') {
//                socket.send(addOrRemoveLike);
//                /* setTimeout(() => {
//                socket_myadmin.send(addOrRemoveLike);
//                }, 500); */
//                event.stopImmediatePropagation();
//                ID = 'x';
//                counter = null;
//                return false;
//            } else {
//                return;
//            }
//
//        });
//    });
//}

//function handleDislikes() {
//    const disLikeForms = document.querySelectorAll('.dislikeform');
//
//    disLikeForms.forEach((form) => {
//        var counter = 1;
//        form.addEventListener('submit', (event) => {
//            event.preventDefault();
//            var ID = form.id.split('-')[1];
//            var addOrRemoveDisLike = JSON.stringify({
//                'id': ID,
//                'type': 'dislike'
//            });
//            if (counter === 1 && ID !== 'x') {
//                socket.send(addOrRemoveDisLike);
//                /* setTimeout(() => {
//                socket_myadmin.send(addOrRemoveLike);
//                }, 500); */
//                event.stopImmediatePropagation();
//                ID = 'x';
//                counter = null;
//                return false;
//            } else {
//                return;
//            }
//
//        });
//    });
//}

function reply_renderer(reply_obj) {
    console.log('THE REPLY OBJ IS', reply_obj)
    var reply_text = reply_obj.reply;
    var new_reply_txt = reply_text.replace(/\</g, '&lt;');
    var new_reply_txt1 = new_reply_txt.replace(/\>/g, '&gt;');

    const new_reply = `
                <ion-card class="ion-no-margin ion-no-padding ion-margin-bottom ">
            <ion-card-header>

                <ion-chip>
                    <ion-avatar>
                        <img src="${ reply_obj.profile_pic }"/>
                    </ion-avatar>
                    <ion-label>
                        ${ reply_obj.username }
                    </ion-label>
                </ion-chip>

                <ion-chip>
                    <ion-label>
                        0 minutes
                    </ion-label>
                </ion-chip>

                <ion-chip class="float-right">
                    <ion-label>
                        ${reply_obj.likes } Likes
                    </ion-label>
                </ion-chip>

            </ion-card-header>
            <ion-card-content class="ion-no-margin ion-no-padding">
<pre class="">
<code style="font-size: 16px">
 ${ new_reply_txt1 }
</code>
</pre>
                <div class="btn-group mb-2 ml-2">
                    <button class="btn btn-primary" id="like-${reply_obj.id}" onclick="handleLike(this)"> ${ reply_obj.likes } Likes </button>
                    <button class="btn-btn-warning" id="dislike-${reply_obj.id}" onclick="handleDisLike(this)"> ${ reply_obj.dislikes } Dislikes </button>
                    <button class="btn btn-info"> 0 Comments </button>
                </div>
                <div class="container p-3 ">
                    <div class="comments-${ reply_obj.id }">
                    <h2 class="text-center"> <ion-title> Comments </ion-title> </h2>

                    </div>


                    <div>
                        <div>
                    <form class="form p-2 commentform" id="form-${reply_obj.id}">
                        <div class="form-group">
                            <textarea class="form-control" rows="5" cols="40" ></textarea>
                        </div>
                        <div class="form-group">
                            <div class="">

                                <button class="btn btn-outline-primary btn-full">
                                    Comment
                                </button>

                            </div>
                        </div>
                    </form>
                    <div class=" p-1">
                        <ion-button class="emojis-show" expand="block" fill="outline" onclick="showEmojis(this)">
                            <ion-chip>
                                &#128512;
                            </ion-chip>
                            <ion-label> Show emojis </ion-label>
                        </ion-button>
                        <div class="comment-emojis fixed-emoji-div" style="display: none">

                        </div>
                    </div>
                            </div>
                </div>

                </div>


            </ion-card-content>
        </ion-card>
            `;

    all_replies_div.insertAdjacentHTML('beforeEnd', new_reply);
    const comment_emojis = document.querySelectorAll('.comment-emojis');
    for (let index = 0; index < comment_emojis.length; index++) {
        CommentEmojis(comment_emojis[index], index)
    }
}

function comment_renderer(comment) {
    console.log('THE COMMENT IS', comment)
    const comment_div = document.querySelector(`.comments-${comment.id}`);
    var comm = comment.comment;
    var new_com = comm.replace(/\</g, '&lt;')
    var new_com1 = new_com.replace(/\>/g, '&gt;')
    const comment_to_render = `
                <div class="mb-1" style="background: var(--ion-color-step-250); border-radius: 10px">
                        <ion-chip color="primary">
                            <ion-avatar slot="">
                                <img src="${comment.profile_pic}" />
                            </ion-avatar>
                            <ion-label> ${ comment.username } </ion-label>
                        </ion-chip>
                        <ion-chip color="primary">
                            0 minutes
                        </ion-chip>

                        <pre class="" >
                            <code style="font-size: 16px; color: var(--ion-color-step-950)" class="com">
  ${ new_com1 }
                            </code>
                        </pre>

                        <div class="btn-group-sm">
                            <button class="btn btn-primary btn-sm"> 2 Likes </button>
                            <button class="btn btn-warning btn-sm"> 4 Dislikes </button>
                            <button class="btn btn-secondary btn-sm"> 3 Comments </button>
                        </div>

                    </div>
            `;
    comment_div.insertAdjacentHTML('beforeEnd', comment_to_render);
}

function like_renderer(like) {
    var like_el = document.querySelector(`#like-${like.id}`);
    var dislike_el = document.querySelector(`#dislike-${like.id}`);
    if (like_el === '') {
        return;
    }
    like_el.innerHTML = like.likes + ' Likes ';
    dislike_el.innerHTML = like.dislikes + ' Dislikes';
}

    function dislike_renderer(like) {
        var dislike_el = document.querySelector(`#dislike-${like.id}`);
        var like_el = document.querySelector(`#like-${like.id}`);
        if (dislike_el === '') {
            return;
        }
        dislike_el.innerHTML = like.dislikes + ' Dislikes';
        like_el.innerHTML = like.likes + ' Likes';
    }


//for (var i = 0; i < document.forms.length; i++) { document.forms[i].style.display = 'none'; }
