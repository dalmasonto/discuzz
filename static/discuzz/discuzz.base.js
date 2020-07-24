async function openMenu() {
     await menuController.open();
}

function goToProfile(){
    window.location.href = '/profile/';
}

function goBack(){
    window.history.back();
}

//function notificationsHandler() {
//    const notification_btn = document.querySelector('#notify');
//    var num = 0;
//    setInterval(() => {
//        notification_btn.innerHTML = num;
//    }, 1000);
//}
//notificationsHandler();