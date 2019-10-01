import Firebase from 'firebase'

// FCM config 정보를 입력하세요
var config = {

  }
Firebase.initializeApp(config)

const messaging = Firebase.messaging()

export { messaging }