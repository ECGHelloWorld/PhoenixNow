importScripts('https://www.gstatic.com/firebasejs/3.5.3/firebase-app.js')
importScripts('https://www.gstatic.com/firebasejs/3.5.3/firebase-messaging.js')

var config = {
  apiKey: "AIzaSyDw6VrOse-Wvpt_d5ZQxYuUITJ36fRhdUo",
  authDomain: "phoenixnow-1a2c0.firebaseapp.com",
  databaseURL: "https://phoenixnow-1a2c0.firebaseio.com",
  storageBucket: "phoenixnow-1a2c0.appspot.com",
  messagingSenderId: "815415960210"
};
firebase.initializeApp(config);


const messaging = firebase.messaging();

messaging.setBackgroundMessageHandler(function(payload) {
  console.log('[firebase-messaging-sw.js] Received background message ', payload);
  // Customize notification here
  const notificationTitle = 'PhoenixNow SignIn';
  const notificationOptions = {
    body: 'Background Message body.'
  };

  return self.registration.showNotification(notificationTitle,
      notificationOptions);
});

//curl 

// curl -X POST --header "Authorization: key=AIzaSyAy7SLrdQIAnauHg0lMGLwYrWaonMMxriE" --Header "Content-Type: application/json" https://fcm.googleapis.com/fcm/send -d "{\"to\":\"fawL7nvcY_g:APA91bFd2HdGqYCqG9-3OG0EGkNerxbbPDnF67vd4zzwhCtoL2rvnuVZ8wAaZ3pM3wI-oS82R5OrvgBolZj2wSVRF089gsWYQYRCA3U1uYB-31UTgKF90jQxy6vK7l-1yEFZSM9UcyXU\",\"notification\":{\"body\":\"Sign In\"},\"title\":\"PhoenixNow\"}"

