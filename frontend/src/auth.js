const self = require('./auth')

export const REDIRECT_URI = 'http://localhost:3000/auth/o/'
export const SUPPORTED_OAUTH_PROVIDERS = ['naver', 'kakao', 'google']

export function buildQuery (url, query) {
  let queries = []
  for (let key in query) {
    queries.push(`${key}=${Boolean(query[key]) ? query[key] : ''}`)
  }
  // if no query, then just return url
  return queries.length > 0 ? (url + '?' + queries.join('&')) : (url)
}

export function getLoginPage (provider) {
  if (SUPPORTED_OAUTH_PROVIDERS.includes(provider)) {
    return self[`${provider.toUpperCase()}_LOGIN_HREF`]
  } else {
    return undefined
  }
}

// required format is: ${provider.toUpperCase()}_LOGIN_HREF
export const NAVER_LOGIN_HREF = buildQuery('https://nid.naver.com/oauth2.0/authorize', {
  response_type: 'code',
  client_id: 'IexPnEMA8XZADrLQY3Bo',
  redirect_uri: buildQuery(REDIRECT_URI, { provider: 'naver' })
})

export const KAKAO_LOGIN_HREF = buildQuery('https://kauth.kakao.com/oauth/authorize', {
  response_type: 'code',
  client_id: 'bc3a3274a103eb12f50fd6c8b43141d2',
  redirect_uri: buildQuery(REDIRECT_URI, { provider: 'kakao' })
})

export const GOOGLE_LOGIN_HREF = buildQuery('https://accounts.google.com/o/oauth2/v2/auth', {
  response_type: 'code',
  client_id: '451025895792-ov19vhj1irvaea4h40f7rm493hir95s2.apps.googleusercontent.com',
  redirect_uri: buildQuery(REDIRECT_URI, { provider: 'google' }),
  scope: 'profile email'
})
