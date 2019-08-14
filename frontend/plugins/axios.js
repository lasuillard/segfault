
function parseCookie (rawCookie) {
  var cookieDict = {}
  rawCookie.split(';').map(cookie => {
    let [k, v] = cookie.split('=')
    cookieDict[decodeURIComponent(k.trim())] = v
  })
  return cookieDict
}

export default function ({ $axios, store }) {
  $axios.onRequest((config) => {
    let token = store.state.user.token
    let csrftoken = parseCookie(document.cookie)['csrftoken']
    
    if (token)
      config.headers.common['Authorization'] = `Token ${token}`
  
    if (csrftoken)
      config.headers.common['X-CSRFTOKEN'] = csrftoken
      
  })
}
