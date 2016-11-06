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
   $("p").append(token);

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
});
