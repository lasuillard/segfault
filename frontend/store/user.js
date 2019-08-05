import $axios from 'axios'
import { getLoginPage } from '~/src/auth'
import { LOAD_TOKEN, SET_TOKEN } from './mutation-types'

const REDIRECT_URI = 'http://localhost:3000/auth/o/'

// used to build querystring
function buildQuery(url, query) {
  let queries = []
  for (let key in query) {
    queries.push(`${key}=${Boolean(query[key]) ? query[key] : ''}`)
  }
  return url + '?' + queries.join('&')
}

export const state = () => ({ 
  token: null,
  provider: null, 
})

export const getters = {
  isLoggedIn: (state) => {
    return Boolean(state.token)
  }
}

export const mutations = {
  [LOAD_TOKEN]: (state) => {
    /*
      load token from browser local storage, if exists
    */
    if (Boolean(localStorage['token'])) {
      state.token = localStorage['token']
    }
  },
  [SET_TOKEN]: (state, { provider, token }) => {
    /*
      set authtoken for api requests
    */
    state.provider = provider
    state.token = token
    $axios.defaults.headers.common['Authorization'] = `Token ${token}`
    localStorage['token'] = token
  },
}

export const actions = {
  loginByLocal (context, credentials) {
    /*
      process local login

      @credentials: account and password
    */
    this.$axios.$post('/rest-auth/login/', {
      username: credentials.account,
      password: credentials.password
    })
    .then(response => {
      context.commit(SET_TOKEN, { 
        provider: 'local', 
        ...response
      })
    })
    .catch(err => {
      console.error(err)
    })
  },
  trySocialLogin (context, provider) { 
    /*
      process login ajax with server
      * in social login, the code is redirected to certain page(/auth/o/^) as query parameter
      * so the client should send this code and obtain token from server

      @provider: social login providers, such as naver, kakao, google, ...
      @return: nothing
    */
    href = getLoginPage(provider)
    if (Boolean(href)) {
      window.location.href = href
    } else {
      console.error(`${provider} is not supported.`)
    }
  },
  finishSocialLogin (context, rsResponse) {
    /*
      obtain token from server with response of resource server(OAuth service provider)
    */
    let { provider } = rsResponse
    delete rsResponse.provider

    this.$axios.$post(`/rest-auth/${provider}/`, { ...rsResponse })
    .then(response => {
      context.commit(SET_TOKEN, {
        provider: provider,
        ...response
      })
      this.$router.replace({ name: 'index' })
    })
    .catch(err => {
      console.error(err)
    })
  },
  logout (context) {
    this.$axios.$post('/rest-auth/logout/')
    .then(response => {
      console.log(response)
    })
    .catch(err => {
      console.error(err)
    })
    .finally(() => {
      context.commit(SET_TOKEN, '')
    })
  },
}
