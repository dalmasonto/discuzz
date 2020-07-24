
 // Participants handler script
const displayEl = document.querySelector('.participants');
loadParticipants();
setInterval(() => {
    loadParticipants();
}, 12000);
loadParticipants();
function loadParticipants() {
    const xhr = new XMLHttpRequest();
    const method = 'GET';
    const link = document.querySelector('.participants-link');
    const url = link.href;
//    console.log(url);

    xhr.open(method, url);
    xhr.onload = () => {
        const response = JSON.parse(xhr.response)
        const participants = response.data
        const childNo = displayEl.childElementCount;
        if (childNo === participants.length) {
            return;
        }
        else if (childNo < participants.length) {
            displayEl.innerHTML = '';
            for (var i = 0; i < participants.length; i++) {
                displayParticipant(participants[i]);

            }
            return;
        }
    }
    xhr.send()
}

function displayParticipant(person) {
    var person = `
                <ion-chip color="success" onclick="view(this)">
                    <ion-avatar class="bg-success"></ion-avatar>
                    <ion-label>
                        ${person}
                    </ion-label>
                </ion-chip>
            `;
    displayEl.insertAdjacentHTML('beforeEnd', person);
}
