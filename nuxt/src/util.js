export function copy (obj) {
  return { ...obj }
}

// source code from https://stackoverflow.com/questions/21741841/detecting-ios-android-operating-system/21742107
export function getUserDeviceType () {
  var userAgent = navigator.userAgent || navigator.vendor || window.opera

  // Windows Phone must come first because its UA also contains "Android"
  if (/windows phone/i.test(userAgent)) {
    return "windows phone"
  }
  
  if (/android/i.test(userAgent)) {
    return "android"
  }
  
  // iOS detection from: http://stackoverflow.com/a/9039885/177710
  if (/iPad|iPhone|iPod/.test(userAgent) && !window.MSStream) {
    return "ios"
  }
  
  return "unknown"
}
