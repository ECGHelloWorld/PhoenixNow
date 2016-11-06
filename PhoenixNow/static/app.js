var config = {
  apiKey: "AIzaSyDw6VrOse-Wvpt_d5ZQxYuUITJ36fRhdUo",
  authDomain: "phoenixnow-1a2c0.firebaseapp.com",
  databaseURL: "https://phoenixnow-1a2c0.firebaseio.com",
  storageBucket: "phoenixnow-1a2c0.appspot.com",
  messagingSenderId: "815415960210"
};
firebase.initializeApp(config);

const messaging = firebase.messaging();

messaging.requestPermission()
.then(function() {
  console.log('Notification permission granted.');
  return messaging.getToken();
})
.then(function(token) {
   console.log(token);
   window.token = token;
   $("#tokenCheck").append(token);

   $.ajax({
    url: "/saveendpoint",
    data: JSON.stringify({
        endpoint: token
    }),
    contentType: 'application/json;charset=UTF-8',
    type: "POST",
    dataType : "json",
   })

   $.ajax({
    headers: {
        'Authorization':'key=AIzaSyAy7SLrdQIAnauHg0lMGLwYrWaonMMxriE',
        'Content-Type':'application/json'
    },
    url: "https://iid.googleapis.com/iid/v1/" + token + "/rel/topics/PhoenixNow",
    type: "POST",
    })

})
.catch(function(err) {
  console.log('Unable to get permission to notify.', err);
});

messaging.onMessage(function(payload) {
  console.log('onMessage: ', payload);
  alert("You are able to successfully receive notifications.")
});

$('#test, #group-status, #opt-out').click(function () {
    if (this.id == 'test') {
        $.ajax({
          headers: {
           'Authorization':'key=AIzaSyAy7SLrdQIAnauHg0lMGLwYrWaonMMxriE',
           'Content-Type':'application/json'
          },
          url: "https://fcm.googleapis.com/fcm/send",
          data: JSON.stringify({
            to: token,
            notification: {"body":"Reminder to Sign In","title":"PhoenixNow","click_action":"https://phoenixnow.org"}
          }),
          contentType: 'application/json',
          type: "POST",
          dataType : "json",
   })
    }
    else if (this.id == 'group-status') {
        $.ajax({
          url: "https://iid.googleapis.com/iid/info/" + token + "?details=true",
          headers: {
            'Authorization':'key=AIzaSyAy7SLrdQIAnauHg0lMGLwYrWaonMMxriE'
          },
          type: "GET",
          dataType : "json",
        }).done(function(msg) {
          console.log(msg)
        });
    }
    else if (this.id == 'opt-out') {
        $.ajax({
        headers: {
            'Authorization':'key=AIzaSyAy7SLrdQIAnauHg0lMGLwYrWaonMMxriE',
            'Content-Type':'application/json'
        },
        url: "https://iid.googleapis.com/iid/v1/" + token + "/rel/topics/PhoenixNow",
        type: "POST",
        })
    }
});
