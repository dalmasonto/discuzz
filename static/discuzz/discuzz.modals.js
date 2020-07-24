
var comments = 0;
var likes = 0;
var dislikes = 0;
var datapoints = [];
customElements.define('modal-content', class extends HTMLElement {
    connectedCallback() {
        const code = document.querySelector('.code').innerHTML;
        const admin = document.querySelector('.admin').innerHTML;
        const topic = document.querySelector('.topic').innerHTML.split(':')[1];
        const subtopic = document.querySelector('.subtopic').innerHTML.split(':')[1];
        const description = document.querySelector('.description').innerHTML;
        const quiz = document.querySelector('#query-text').innerHTML;

        this.innerHTML = `
          <ion-header>
            <ion-toolbar color="primary">
              <ion-title> Question statistics </ion-title>
              <ion-buttons slot="end">
                <ion-button id='close' onclick="dismissModall()">Close</ion-button>
              </ion-buttons>
            </ion-toolbar>
          </ion-header>
          <ion-content fullscreen>
          <h4 class="text-center"> Statistics details for ${code} </h4>
          <ion-card>
            <ion-card-header>
                <ion-chip color="primary">
                    <ion-label> <h4 class="text-center"> Admin - ${admin} </h4> </ion-label>
                </ion-chip>

                <ion-chip color="primary">
                    <ion-label> <h5 class="text-center"> Topic - ${topic} </h5> </ion-label>
                </ion-chip>

                <ion-chip color="primary">
                    <ion-label> <h5 class="text-center"> Subtopic - ${subtopic} </h5> </ion-label>
                </ion-chip>

                </ion-card-header>
                <ion-card-content>

                    <ion-card-subtitle color="warning"> Question </ion-card-subtitle>
                        <ion-chip color="primary">
                            <ion-label> <p class="text-success ion-no-margin ion-no-padding"> Description - ${description} </p> </ion-label>
                        </ion-chip>
                        <pre class="text-dark ion-no-margin ion-no-padding"> 
${quiz} 
                        </pre>
                </ion-card-content>
                </ion-card>

            <ion-list class="u-reply">


            </ion-list>

            <div id="chartContainer" style="height: 370px; max-width: 920px; margin: 0px auto;"></div>

            </ion-card-content>

          </ion-card>
         </ion-content>
        `;
    }
});

function xhr() {
    const discussion_api_link = document.querySelector('.discussion-link');
    const xhr = new XMLHttpRequest();
    const method = 'GET';

    xhr.open(method, discussion_api_link);
    xhr.onload = () => {
        var response = JSON.parse(xhr.response);
        var data = response.response;

        for (var i = 0; i < data.length; i++) {
            renderReply(data[i]);
            comments += data[i].comments;
            likes += data[i].likes;
            dislikes += data[i].dislikes;
        }
        var total = comments + likes + dislikes;
        var comper = Math.round((comments / total) * 100);
        var likesper = Math.round((likes / total) * 100);
        var dislikesper = Math.round((dislikes / total) * 100);

        datapoints = [
            { y: comper, name: 'comments' },
            { y: likesper, name: 'likes' },
            { y: dislikesper, name: 'dislikes' },
        ]
        var chart = new CanvasJS.Chart("chartContainer", {
            exportEnabled: true,
            animationEnabled: true,
            title: {
                text: "Question statistics"
            },
            legend: {
                cursor: "pointer",
                itemclick: explodePie
            },
            data: [{
                type: "pie",
                showInLegend: true,
                toolTipContent: "{name}: <strong>{y}%</strong>",
                indexLabel: "{name} - {y}%",
                dataPoints: datapoints
            }]
        });

        chart.render();

    }
    xhr.send()

}



function limitReplyLength(reply, limit = 30) {
    const limitedReply = [];
    if (reply.length > limit) {
        reply.split(' ').reduce((acc, cur) => {
            if (acc.length <= limit) {
                limitedReply.push(cur);
            }
            return acc + cur.length;
        }, 0)
        return `${limitedReply.join(' ')}... a long reply)`;
    }
    return reply;
}

function explodePie(e) {
    if (typeof (e.dataSeries.dataPoints[e.dataPointIndex].exploded) === "undefined" || !e.dataSeries.dataPoints[e.dataPointIndex].exploded) {
        e.dataSeries.dataPoints[e.dataPointIndex].exploded = true;
    } else {
        e.dataSeries.dataPoints[e.dataPointIndex].exploded = false;
    }
    e.chart.render();

}
function renderReply(reply) {
    const u_reply = document.querySelector('.u-reply');
    var rep = reply.reply;
    var new_reply = rep.replace(/\</g, '&lt;')
    var new_reply1 = new_reply.replace(/\>/g, '&gt;')
    var replyToRender = limitReplyLength(new_reply1, 30)
    var el = `
                <ion-card color="dark" class="ion-no-padding ion-no-margin">
                    <ion-card-header>
                        <ion-item color="warning">

                            <ion-avatar slot="start">
                                <ion-img src="${reply.pic}"/>
                            </ion-avatar>

                            <ion-label class="w-100">
                                <h2 class="text-dark">${reply.username}</h2>
                                <h3 class="text-dark">${reply.reply_time}</h3>
                            </ion-label>

                        </ion-item>

                    </ion-card-header>
                    <ion-card-content>
                        <div>
                            <p class="text-dark">${replyToRender}</p>
                        </div>
                        <div>
                            <ion-chip color="primary>

                                <ion-label class="ion-margin-right"> Comments </ion-label>
                                <ion-badge> ${reply.comments} </ion-badge>

                            </ion-chip>
                            <ion-chip color="success">
                                <ion-icon name="thumbs-up-sharp"></ion-icon>
                                <ion-label class="ion-margin-right"> Likes </ion-label>
                                <ion-badge> ${reply.likes} </ion-badge>

                            </ion-chip>
                            <ion-chip color="danger">
                                <ion-icon name="thumbs-down-sharp"></ion-icon>
                                <ion-label class="ion-margin-right"> Dislikes </ion-label>
                                <ion-badge> ${reply.dislikes} </ion-badge>

                            </ion-chip>
                        </div>
                    <ion-card-content>

                </ion-card>
            `;
    u_reply.insertAdjacentHTML('beforeEnd', el);
}

let currentModal = null;
// const button = document.querySelector('ion-button');
// button.addEventListener('click', createModal);

async function presentAnalyticsModal() {
    const modal = await modalController.create({
        component: 'modal-content'
    });

    await modal.present();
    setTimeout(() => {
        xhr();
    }, 2000);
    currentModal = modal;
}

function dismissModall() {
    if (currentModal) {
        currentModal.dismiss().then(() => { currentModal = null; });
    }
}



customElements.define('user-content', class extends HTMLElement {
    connectedCallback() {
        this.innerHTML = `
          <ion-header>
            <ion-toolbar color="primary">
              <ion-title class="user-name">  </ion-title>
              <ion-buttons slot="end">
                <ion-button color="danger" id='cloose' onclick="dismissModal()">
                    <ion-icon name="close"></ion-icon>
                    <ion-label> Close </ion-label>
                </ion-button>
              </ion-buttons>
            </ion-toolbar>
          </ion-header>
          <ion-content fullscreen color="">
          <h4 class="text-center"> User profile </h4>
          <ion-card color="dark">
            <ion-card-header>

                <ion-avatar class='' style="height: 250px; width: 250px; margin: auto; max-width: 100%;">
                    <img class='u-img ' style="-webkit-user-select: none;max-width: 100%;margin: 0;cursor: zoom-in;">
                </ion-avatar>

            </ion-card-header>
            <ion-card-content class="ion-no-padding">

                <ion-item class="ion-no-padding">
                    <ion-label class="ion-no-padding"> <p class="text-dark ion-no-padding"> <span class='f-name'></span> </p> </ion-label>
                </ion-item>

                <ion-item>
                    <ion-label> <p class="text-dark ion-no-padding"> <span class='l-name'></span> </p> </ion-label>
                </ion-item>

                <ion-item>
                    <ion-label> <p class="text-dark ion-no-padding"> <span class='e-name'></span> </p> </ion-label>
                </ion-item>

                <ion-item>
                    <ion-label> <p class="text-dark ion-no-padding"> <span class='u-name'></span> </p> </ion-label>
                </ion-item>

            </ion-card-content>
           </ion-card>

           <ion-card color="dark">
            <ion-card-header>

                <ion-card-title class='w-100 text-center text-primary'>
                    <h3 class="ion-animate"> Participation details </h3>
                </ion-card-title>

            </ion-card-header>
            <ion-card-content class="ion-no-padding">

                <div class="text-dark t-name w-100 ion-no-padding"> </div>
                <div class="text-dark s-name w-100 ion-no-margin"> </div>
                <div class="text-dark q-name w-100 ion-no-padding"> </div>
                <div class="text-dark r-name w-100 ion-no-padding"> </div>
                <div class="text-dark c-name w-100 ion-no-padding"> </div>

            </ion-card-content>
           </ion-card>

           <ion-card-footer id="add-send-button">

           </ion-card-footer>

          </ion-content>
        `;
    }
});



let currentModal1 = null;


async function view(el) {
    // create the modal with the `modal-page` component
    const modalElement = document.createElement('ion-modal');
    modalElement.component = 'user-content';
    modalElement.cssClass = 'my-custom-class';


    var name = el.children[1].innerHTML.trim();

    // present the modal
    document.body.appendChild(modalElement);

    window.setTimeout(() => {

        const xhr = new XMLHttpRequest();
        const method = 'GET';
        const link = `/api/user-details/${name}/`;
        console.log(link);

        xhr.open(method, link);
        xhr.onload = () => {
            const response = xhr.response;
            var data = JSON.parse(response);
            console.log(data)

            var pic = data['user']['pic'];
            var first_name = data['user']['first'];
            var last_name = data['user']['last'];
            var email = data['user']['email'];
            var username = data['user']['username'];

            var topics = data['topics'];
            var subtopics = data['topics'];
            var quizes = data['quizes'];
            var replies = data['replies'];
            var comments = data['comments'];

            var firstPlace = document.querySelector('.f-name');
            var lastPlace = document.querySelector('.l-name');
            var emailPlace = document.querySelector('.e-name');
            var namePlace = document.querySelector('.u-name');
            var picPlace = document.querySelector('.u-img');
            var addSendButton = document.querySelector('#add-send-button');

            var userPlace = document.querySelector('.user-name');
            var topicPlace = document.querySelector('.t-name');
            var subtopicPlace = document.querySelector('.s-name');
            var quizesPlace = document.querySelector('.q-name');
            var repliesPlace = document.querySelector('.r-name');
            var commentsPlace = document.querySelector('.c-name');

            picPlace.src = pic;
            firstPlace.innerHTML = 'First name - ' + first_name;
            lastPlace.innerHTML = 'First name - ' + last_name;
            emailPlace.innerHTML = 'First name - ' + email;
            namePlace.innerHTML = 'Username - ' + username;
            userPlace.innerHTML = username;
            addSendButton.innerHTML = `
            <a class="btn btn-primary w-100" href="/chat/${username}"> Send direct message  </a>
            `;


            topicPlace.innerHTML = `
                        <ion-chip color="primary" class="w-100">
                            <ion-badge > Topicss </ion-badge>
                            <ion-label class="ion-padding float-right"> ${topics} </ion-label>
                        </ion-chip>
                    `;
            subtopicPlace.innerHTML = `
                        <ion-chip color="warning" class="w-100">
                            <ion-badge> Subtopics </ion-badge>
                            <ion-label class="ion-padding float-right"> ${subtopics} </ion-label>
                        </ion-chip>
                    `;
            quizesPlace.innerHTML = `
                    <ion-chip color="primary" class="w-100">
                        <ion-badge> Questions </ion-badge>
                        <ion-label class="ion-padding float-right"> ${quizes} </ion-label>
                    </ion-chip>
                    `;
            repliesPlace.innerHTML = `
                    <ion-chip color="warning" class="w-100">
                        <ion-badge> Replies </ion-badge>
                        <ion-label class="ion-padding float-right"> ${replies} </ion-label>
                    </ion-chip>
                    `;
            commentsPlace.innerHTML = `
                    <ion-chip color="primary" class="w-100">
                        <ion-badge> Comments </ion-badge>
                        <ion-label class="ion-padding float-right"> ${comments} </ion-label>
                    </ion-chip>
                    `;
        }
        xhr.send()

    }, 1000);




    await modalElement.present();

    currentModal1 = modalElement;
}



async function modal() {
    const modal = await modalController.create({
        component: 'user-content'
    });


    await modal.present();

    currentModal1 = modal;
}

function dismissModal() {
    if (currentModal1) {
        currentModal1.dismiss().then(() => { currentModal1 = null; });
    }
}

async function presentActionSheet() {
    const actionSheet = document.createElement('ion-action-sheet');

    actionSheet.header = 'Albums';
    actionSheet.cssClass = 'my-custom-class';
    actionSheet.mode = 'ios';
    actionSheet.buttons = [{
        text: 'Delete',
        role: 'destructive',
        icon: 'trash',
        handler: () => {
            console.log('Delete clicked');
        }
    }, {
        text: 'Share',
        icon: 'share',
        handler: () => {
            console.log('Share clicked');
        }
    }, {
        text: 'Play (open modal)',
        icon: 'caret-forward-circle',
        handler: () => {
            console.log('Play clicked');
        }
    }, {
        text: 'Favorite',
        icon: 'heart',
        handler: () => {
            console.log('Favorite clicked');
        }
    }, {
        text: 'Cancel',
        icon: 'close',
        role: 'cancel',
        handler: () => {
            console.log('Cancel clicked');
        }
    }];
    document.body.appendChild(actionSheet);
    return actionSheet.present();
}

var slides = document.querySelector('ion-slides');

// Optional parameters to pass to the swiper instance.
// See http://idangero.us/swiper/api/ for valid options.
slides.options = {
    initialSlide: 1,
    speed: 100,

}

const slideOpts = {
    on: {
        beforeInit() {
            const swiper = this;
            swiper.classNames.push(`${swiper.params.containerModifierClass}flip`);
            swiper.classNames.push(`${swiper.params.containerModifierClass}3d`);
            const overwriteParams = {
                slidesPerView: 1,
                slidesPerColumn: 1,
                slidesPerGroup: 1,
                watchSlidesProgress: true,
                spaceBetween: 0,
                virtualTranslate: true,
            };
            swiper.params = Object.assign(swiper.params, overwriteParams);
            swiper.originalParams = Object.assign(swiper.originalParams, overwriteParams);
        },
        setTranslate() {
            const swiper = this;
            const { $, slides, rtlTranslate: rtl } = swiper;
            for (let i = 0; i < slides.length; i += 1) {
                const $slideEl = slides.eq(i);
                let progress = $slideEl[0].progress;
                if (swiper.params.flipEffect.limitRotation) {
                    progress = Math.max(Math.min($slideEl[0].progress, 1), -1);
                }
                const offset$$1 = $slideEl[0].swiperSlideOffset;
                const rotate = -180 * progress;
                let rotateY = rotate;
                let rotateX = 0;
                let tx = -offset$$1;
                let ty = 0;
                if (!swiper.isHorizontal()) {
                    ty = tx;
                    tx = 0;
                    rotateX = -rotateY;
                    rotateY = 0;
                } else if (rtl) {
                    rotateY = -rotateY;
                }

                $slideEl[0].style.zIndex = -Math.abs(Math.round(progress)) + slides.length;

                if (swiper.params.flipEffect.slideShadows) {
                    // Set shadows
                    let shadowBefore = swiper.isHorizontal() ? $slideEl.find('.swiper-slide-shadow-left') : $slideEl.find('.swiper-slide-shadow-top');
                    let shadowAfter = swiper.isHorizontal() ? $slideEl.find('.swiper-slide-shadow-right') : $slideEl.find('.swiper-slide-shadow-bottom');
                    if (shadowBefore.length === 0) {
                        shadowBefore = swiper.$(`<div class="swiper-slide-shadow-${swiper.isHorizontal() ? 'left' : 'top'}"></div>`);
                        $slideEl.append(shadowBefore);
                    }
                    if (shadowAfter.length === 0) {
                        shadowAfter = swiper.$(`<div class="swiper-slide-shadow-${swiper.isHorizontal() ? 'right' : 'bottom'}"></div>`);
                        $slideEl.append(shadowAfter);
                    }
                    if (shadowBefore.length) shadowBefore[0].style.opacity = Math.max(-progress, 0);
                    if (shadowAfter.length) shadowAfter[0].style.opacity = Math.max(progress, 0);
                }
                $slideEl
                    .transform(`translate3d(${tx}px, ${ty}px, 0px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`);
            }
        },
        setTransition(duration) {
            const swiper = this;
            const { slides, activeIndex, $wrapperEl } = swiper;
            slides
                .transition(duration)
                .find('.swiper-slide-shadow-top, .swiper-slide-shadow-right, .swiper-slide-shadow-bottom, .swiper-slide-shadow-left')
                .transition(duration);
            if (swiper.params.virtualTranslate && duration !== 0) {
                let eventTriggered = false;
                // eslint-disable-next-line
                slides.eq(activeIndex).transitionEnd(function onTransitionEnd() {
                    if (eventTriggered) return;
                    if (!swiper || swiper.destroyed) return;

                    eventTriggered = true;
                    swiper.animating = false;
                    const triggerEvents = ['webkitTransitionEnd', 'transitionend'];
                    for (let i = 0; i < triggerEvents.length; i += 1) {
                        $wrapperEl.trigger(triggerEvents[i]);
                    }
                });
            }
        }
    }
};

function presentAlert() {
    const alert = document.createElement('ion-alert');
    alert.cssClass = 'my-custom-class';
    alert.mode = 'ios';
    alert.header = 'Alert';
    alert.subHeader = 'Subtitle';
    alert.message = 'This is an alert message.';
    alert.buttons = ['OK'];

    document.body.appendChild(alert);
    return alert.present();
}

function presentAlertMultipleButtons() {
    const alert = document.createElement('ion-alert');
    alert.cssClass = 'my-custom-class';
    alert.header = 'Alert';
    alert.mode = 'ios';
    alert.subHeader = 'Subtitle';
    alert.message = 'This is an alert message.';
    alert.buttons = ['Cancel', 'Open Modal', 'Delete'];

    document.body.appendChild(alert);
    return alert.present();
}

function presentAlertConfirm() {
    const alert = document.createElement('ion-alert');
    alert.cssClass = 'my-custom-class';
    alert.header = 'Confirm!';
    alert.mode = 'ios';
    alert.message = 'Message <strong>text</strong>!!!';
    alert.buttons = [
        {
            text: 'Cancel',
            role: 'cancel',
            cssClass: 'secondary',
            handler: (blah) => {
                console.log('Confirm Cancel: blah');
            }
        }, {
            text: 'Okay',
            handler: () => {
                console.log('Confirm Okay')
            }
        }
    ];

    document.body.appendChild(alert);
    return alert.present();
}

function presentAlertPrompt() {
    const alert = document.createElement('ion-alert');
    alert.cssClass = 'my-custom-class';
    alert.header = 'Prompt!';
    alert.mode = 'ios';
    alert.inputs = [
        {
            placeholder: 'Placeholder 1'
        },
        {
            name: 'name2',
            id: 'name2-id',
            value: 'hello',
            placeholder: 'Placeholder 2'
        },
        // multiline input.
        {
            name: 'paragraph',
            id: 'paragraph',
            type: 'textarea',
            placeholder: 'Placeholder 3'
        },
        {
            name: 'name3',
            value: 'http://ionicframework.com',
            type: 'url',
            placeholder: 'Favorite site ever'
        },
        // input date with min & max
        {
            name: 'name4',
            type: 'date',
            min: '2017-03-01',
            max: '2018-01-12'
        },
        // input date without min nor max
        {
            name: 'name5',
            type: 'date'
        },
        {
            name: 'name6',
            type: 'number',
            min: -5,
            max: 10
        },
        {
            name: 'name7',
            type: 'number'
        },
        {
            name: 'name8',
            type: 'password',
            placeholder: 'Advanced Attributes',
            cssClass: 'specialClass',
            attributes: {
                maxlength: 4,
                inputmode: 'decimal'
            }
        }
    ];
    alert.buttons = [
        {
            text: 'Cancel',
            role: 'cancel',
            cssClass: 'secondary',
            handler: () => {
                console.log('Confirm Cancel')
            }
        }, {
            text: 'Ok',
            handler: () => {
                console.log('Confirm Ok')
            }
        }
    ];

    document.body.appendChild(alert);
    return alert.present();
}

function presentAlertRadio() {
    const alert = document.createElement('ion-alert');
    alert.cssClass = 'my-custom-class';
    alert.header = 'Radio';
    alert.mode = 'ios';
    alert.inputs = [
        {
            type: 'radio',
            label: 'Radio 1',
            value: 'value1',
            checked: true
        },
        {
            type: 'radio',
            label: 'Radio 2',
            value: 'value2'
        },
        {
            type: 'radio',
            label: 'Radio 3',
            value: 'value3'
        },
        {
            type: 'radio',
            label: 'Radio 4',
            value: 'value4'
        },
        {
            type: 'radio',
            label: 'Radio 5',
            value: 'value5'
        },
        {
            type: 'radio',
            label: 'Radio 6 Radio 6 Radio 6 Radio 6 Radio 6 Radio 6 Radio 6 Radio 6 Radio 6 Radio 6 ',
            value: 'value6'
        }
    ];
    alert.buttons = [
        {
            text: 'Cancel',
            role: 'cancel',
            cssClass: 'secondary',
            handler: () => {
                console.log('Confirm Cancel')
            }
        }, {
            text: 'Ok',
            handler: () => {
                console.log('Confirm Ok')
            }
        }
    ];
    document.body.appendChild(alert);
    return alert.present();
}

function presentAlertCheckbox() {
    const alert = document.createElement('ion-alert');
    alert.cssClass = 'my-custom-class';
    alert.header = 'Checkbox';
    alert.mode = 'ios';
    alert.inputs = [
        {
            type: 'checkbox',
            label: 'Checkbox 1',
            value: 'value1',
            checked: true
        },

        {
            type: 'checkbox',
            label: 'Checkbox 2',
            value: 'value2'
        },

        {
            type: 'checkbox',
            label: 'Checkbox 3',
            value: 'value3'
        },

        {
            type: 'checkbox',
            label: 'Checkbox 4',
            value: 'value4'
        },

        {
            type: 'checkbox',
            label: 'Checkbox 5',
            value: 'value5'
        },

        {
            type: 'checkbox',
            label: 'Checkbox 6 Checkbox 6 Checkbox 6 Checkbox 6 Checkbox 6 Checkbox 6 Checkbox 6 Checkbox 6 Checkbox 6 Checkbox 6',
            value: 'value6'
        }
    ];
    alert.buttons = [
        {
            text: 'Cancel',
            role: 'cancel',
            cssClass: 'secondary',
            handler: () => {
                console.log('Confirm Cancel')
            }
        }, {
            text: 'Ok',
            handler: () => {
                console.log('Confirm Ok')
            }
        }
    ];

    document.body.appendChild(alert);
    return alert.present();
}


const API_KEY = 'be64b79bc5a54295bde012c21cc488e3';
const endpoint = 'https://cors-anywhere.herokuapp.com/https://newsapi.org/v2/top-headlines?country=us&apiKey=be64b79bc5a54295bde012c21cc488e3';
var news = fetch(endpoint);
console.log(news);
