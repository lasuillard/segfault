import $axios from 'axios'
import { getLoginPage } from '~/src/auth'
import { SET_TOKEN, DELETE_TOKEN } from './mutation-types'


export const state = () => ({
  avatar: null,
  username: null,
  email: null,
  token: null
})

export const getters = {
  getUserProfile: (state) => {
    return {
      avatar: state.avatar || '',
      username: state.username || 'Guest',
      email: state.email || 'No email has been set.'
    }
  },
  isLoggedIn: (state) => {
    return Boolean(state.token)
  }
}

export const mutations = {
  [SET_TOKEN]: (state, token) => {
    /*
      set authtoken for api requests
    */
    state.token = token
    $axios.defaults.headers.common['Authorization'] = `Token ${token}`
    localStorage.setItem('token', token)
  },
  [DELETE_TOKEN]: (state) => {
    /*
      delete token from browser local storage
    */
    state.token = null
    localStorage.removeItem('token')
  }
}

export const actions = {
  loadToken (context) {
    /*
      load token from browser local storage, if exists

      @return: nothing
    */
    let storedToken = localStorage.getItem('token')
    if (Boolean(storedToken)) {
      context.commit(SET_TOKEN, storedToken)
    }
  },
  loginByLocal (context, credentials) {
    /*
      process local login

      @credentials: account and password
      @return: nothing
    */
    this.$axios.$post('/rest-auth/login/', {
      username: credentials.account,
      password: credentials.password
    })
    .then(response => {
      context.commit(SET_TOKEN, response.token)
      this.$router.push({ name: 'user' })
    })
    .catch(err => {
      console.error(err)
    })
  },
  trySocialLogin (context, provider) { 
    /*
      process login ajax with server
      * in social login, the code is redirected to certain page(/auth/o/) as query parameter
      * so the client should send this code and obtain token from server

      @provider: social login providers, such as naver, kakao, google, ...
      @return: nothing
    */
    let href = getLoginPage(provider)
    if (Boolean(href)) {
      window.location.href = href
    } else {
      console.error(`${provider} is not supported.`)
    }
  },
  finishSocialLogin (context, rsResponse) {
    /*
      obtain token from server with response of resource server(OAuth service provider)

      @rsResponse: the response of resource server(google, ...)
      @return: nothing
    */
    let { provider } = rsResponse
    delete rsResponse.provider // no need to send server, just for routing

    this.$axios.$post(`/rest-auth/${provider}/`, { ...rsResponse })
    .then(response => {
      context.commit(SET_TOKEN, response.token)
      this.$router.replace({ name: 'index' })
    })
    .catch(err => {
      // TODO: replace route to error page
      console.error(err)
    })
  },
  logout (context) {
    /*
      notify server user is logging out

      @return nothing
    */
    this.$axios.$post('/rest-auth/logout/')
    .then(response => {
      console.log(response)
    })
    .catch(err => {
      console.error(err)
    })
    .finally(() => {
      context.commit(DELETE_TOKEN)
    })
  },
}
