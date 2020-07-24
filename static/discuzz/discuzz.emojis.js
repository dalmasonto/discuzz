
const emojis = document.querySelector('.emojis');
const emojis_one = document.querySelector('.emojis-one');
const emojis_two = document.querySelector('.emojis-two');
const emojis_more = document.querySelector('.emojis-more');
var btns = document.querySelectorAll('.emoji-show');

const comment_emojis = document.querySelectorAll('.comment-emojis');

var text = document.querySelector('#reply');

function addCommentEmoji(num) {
    window.addEventListener('dblclick', (e) => {
        e.preventDefault();
    });
    var btn = num.parentNode.parentNode.children[0].children[0].children[1];
    var text_area = num.parentNode.parentNode.parentNode.children[3].children[1].children[1].children[0].children[0].children[0].children[1].children[1].children[1];
    console.log(btn)
    var parent_emojis_div = num.parentNode;
    
    console.log('the btn ', btn);
    text_area.addEventListener('click', () => {
        parent_emojis_div.style.display = 'none';
        btn.innerHTML = 'Show Emojis';
    });
    text_area.value += num.textContent;

}

function showEmojis(btn) {
    const emoji_div = btn.parentNode.parentNode.children[1];
    const label = btn.children[1];
    const style = emoji_div.style.display;

    if (style === 'block') {
        label.innerHTML = 'Show Emojis';
        emoji_div.style.display = 'none';
    }
    else if (style === 'none') {
        label.innerHTML = 'Hide Emojis';
        emoji_div.style.display = 'block';
    }

}

function CommentEmojis(field, index) {

    for (let index = 0; index < 1000; index++) {
        var num = 127744 + index;
        var emoji = `<span class="spaced" onclick='addCommentEmoji(this)'>&#${num};</span>`;
        field.insertAdjacentHTML('beforeEnd', emoji);
    }

}

for (let index = 0; index < comment_emojis.length; index++) {
    CommentEmojis(comment_emojis[index], index)
}

function createEmojis(index) {
    var num = 128512 + index;
    var emoji = `<span class="spaced" onclick='addEmoji(this)'>&#${num};</span>`;
    emojis.insertAdjacentHTML('beforeEnd', emoji);
}

function createEmojisOne(index) {
    var num = 129293 + index;
    var emoji = `<span class="spaced" onclick='addEmoji(this)'>&#${num};</span>`;
    emojis_one.insertAdjacentHTML('beforeEnd', emoji);
}

function createEmojisTwo(index) {
    var num = 128650 + index;
    var emoji = `<span class="spaced primary" onclick='addEmoji(this)'>&#${num};</span>`;
    emojis_two.insertAdjacentHTML('beforeEnd', emoji);
}

function MoreEmojis(index) {
    var num = 119808 + index;
    var emoji = `<span class="spaced" onclick='addEmoji(this)'>&#${num};</span>`;
    emojis_more.insertAdjacentHTML('beforeEnd', emoji);
}

for (let index = 0; index < 80; index++) {
    createEmojis(index);
}
for (let index = 0; index < 243; index++) {
    createEmojisOne(index);
}
for (let index = 0; index < 100; index++) {
    createEmojisTwo(index);
}
for (let index = 0; index < 1024; index++) {
    MoreEmojis(index);
}

function addEmoji(num) {
    window.addEventListener('dblclick', (e) => {
        e.preventDefault();
    });
    var inner = text.textContent;
    var em = `&#${num}`;
    text.value += num.textContent
}

