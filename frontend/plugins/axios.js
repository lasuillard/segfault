
function parseCookie (rawCookie) {
  var cookieDict = {}
  rawCookie.split(';').map(cookie => {
    var arr = cookie.trim().split('=')
    cookieDict[arr[0]] = arr[1]
  })
  return cookieDict
}

export default function ({ $axios, store }) {
  $axios.onRequest((config) => {

  })
 }
