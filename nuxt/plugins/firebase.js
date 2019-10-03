import firebase from 'firebase'

var firebaseConfig = {
  apiKey: "AIzaSyCRxyiBRGBJPUFY_z7nNLPoPEltTiVoDCE",
  authDomain: "segfault-24a1e.firebaseapp.com",
  databaseURL: "https://segfault-24a1e.firebaseio.com",
  projectId: "segfault-24a1e",
  storageBucket: "",
  messagingSenderId: "745382831176",
  appId: "1:745382831176:web:c88ee1be911f9a1275e47d",
  measurementId: "G-1RC5S7R9N1"
};
firebase.initializeApp(firebaseConfig);
const messaging = firebase.messaging()

export { messaging }
