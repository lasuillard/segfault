import axios from 'axios'
import { getLoginPage } from '~/src/auth'
import { SET_TOKEN, SET_USER, SET_AVATAR, SET_CONFIG } from './mutation-types'


export const state = () => ({
  token: null,
  user: {
    pk: null,
    username: null,
    email: null
  },
  avatar: {
    pk: null,
    profile_image: null,
    display_name: null,
    introduce_message: '',
  },
  config: {
    theme: 'light'
  }
})

export const getters = {
  isLoggedIn: (state) => {
    return Boolean(state.token)
  },
  getUserProfile: (state) => {
    let { user, avatar } = state
    return {
      display_name: avatar.display_name || user.username || 'Guest',
      username: user.username || 'Guest',
      email: user.email || 'No email has been set.',
      profile_image: avatar.profile_image || ''
    }
  },
  getConfig: (state) => {
    return state.config || {}
  },
}

export const mutations = {
  [SET_TOKEN]: (state, token) => {
    /*
      set authtoken for api requests
    */
    if (token == null) {
      state.token = null
      axios.defaults.headers.common['Authorization'] = null
      localStorage.removeItem('token')
    } else {
      state.token = token
      axios.defaults.headers.common['Authorization'] = `Token ${token}`
      localStorage.setItem('token', token)
    }
  },
  [SET_USER]: (state, user) => {
    let obj = state.user

    obj.pk = user.pk
    obj.username = user.username
    obj.email = user.email
  },
  [SET_AVATAR]: (state, avatar) => {
    let obj = state.avatar

    obj.pk = avatar.pk
    obj.display_name = avatar.display_name
    obj.profile_image = avatar.profile_image
    obj.introduce_message = avatar.introduce_message
  },
  [SET_CONFIG]: (state, config) => {
    state.config = config
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
      return context.dispatch('afterLogin', {
        token: response.token,
        user: response.user
      })
    })
    .then(() => {
      this.$router.replace({ name: 'user' })
    })
    .catch(err => {
      console.log(err.response.data)
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
      return context.dispatch('afterLogin', {
        token: response.token,
        user: response.user
      })
    })
    .then(() => {
      this.$router.replace({ name: 'user' })
    })
    .catch(err => {
      // TODO: replace route to error page
      console.log(err)
    })
  },
  afterLogin (context, { token, user }) {
    context.commit(SET_TOKEN, token)
    context.commit(SET_USER, user)
    return new Promise((resolve, reject) => {
      this.$axios.$get(`/api/avatar/${user.avatar}`)
      .then(response => {
        context.commit(SET_AVATAR, response)
        resolve()
      })
      .catch(err => reject(err))
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
      context.commit(SET_TOKEN, null)
    })
  },
  saveConfig (context, config) {
    context.commit(SET_CONFIG, config)
    if (!context.getters.isLoggedIn)
      return

    this.$axios.$patch(`/api/avatar/${context.state.avatar.pk}/`, {
      user_data: {
        config: context.state.config
      }
    })
    .then(response => {
      console.log(response)
    })
    .catch(err => {
      console.log(err.response.data)
    })
  }
}
