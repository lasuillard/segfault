import Vue from 'vue'
import { getLoginPage } from '~/src/auth'
import { SET_TOKEN, SET_USER, SET_AVATAR, SET_CONFIG } from './mutation-types'


export const state = () => ({
  token: null,
  user: {
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
    // return login status of user
    return Boolean(state.token)
  },
  getUserProfile: (state) => {
    // return user profile
    let { user, avatar } = state
    return {
      display_name: avatar.display_name || 'Guest',
      email: user.email || 'No e-mail',
      profile_image: avatar.profile_image || ''
    }
  },
  getConfig: (state) => {
    // return user application setting
    return state.config || {}
  },
}

export const mutations = {
  [SET_TOKEN]: (state, token) => {
    // store token. request headers will be handled on plugins.
    if (token == null) {
      state.token = null
      localStorage.removeItem('token')
    } else {
      state.token = token
      localStorage.setItem('token', token)
    }
  },
  [SET_USER]: (state, user) => {
    // set user identification
    let obj = state.user
    obj.email = user.email
  },
  [SET_AVATAR]: (state, avatar) => {
    // set additional user information
    let obj = state.avatar
    obj.pk = avatar.pk
    obj.display_name = avatar.display_name
    obj.profile_image = avatar.profile_image
    obj.introduce_message = avatar.introduce_message
  },
  [SET_CONFIG]: (state, config) => {
    /*
      set config locally (no request to server to store it)

      anonymous users can change settings but is volatile
    */
    state.config = config
  }
}

export const actions = {
  loadToken (context) {
    /*
      load token from certain storage

      this is reserved as vuex actions to support storage requires asynchronous behaviors
    */
    return new Promise((resolve, reject) => {
      if (true) {
        let storedToken = localStorage.getItem('token')
        if (Boolean(storedToken)) {
          context.commit(SET_TOKEN, storedToken)
        }
      } else {
        // just an placeholder
        resolve()
      }
    })
  },
  loginByLocal (context, credentials) {
    // process local login
    return new Promise((resolve, reject) => {
      this.$axios.$post('/rest-auth/login/', {
        email: credentials.email,
        password: credentials.password
      })
      .then(response => {
        return context.dispatch('afterLogin', {
          token: response.key,
        })
      })
      .then(() => {
        this.$router.replace({ name: 'user' })
        resolve()
      })
      .catch(err => {
        console.log(err.response.data)
        reject()
      })
    })
  },
  trySocialLogin (context, provider) { 
    /*
      process login ajax with server
      
      in social login, the code is redirected to certain page(/auth/o/) as query parameter
      so the client should send this code and obtain token from server
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
      obtain authentication token from server

      it should be used with trySocialLogin actions as pair
      this action will pack querystring into body and send it to server to get token
      @rsResponse: the response of resource server(google, ...)
    */
    return new Promise((resolve, reject) => {
      let { provider } = rsResponse
      delete rsResponse.provider // no need to send server, just for routing
      this.$axios.$post(`/rest-auth/${provider}/`, { ...rsResponse })
      .then(response => {
        return context.dispatch('afterLogin', {
          token: response.key,
        })
      })
      .then(() => {
        this.$router.replace({ name: 'user' })
        resolve()
      })
      .catch(err => {
        console.log(err)
        reject()
      })
    })
  },
  afterLogin (context, { token }) {
    // load user profile from server with authtoken
    return new Promise((resolve, reject) => {
      context.commit(SET_TOKEN, token)
      this.$axios.$get(`/rest-auth/user/`)
      .then(response => {
        context.commit(SET_USER, {
          email: response.email
        })
        context.commit(SET_AVATAR, response.avatar)
        context.commit(SET_CONFIG, response.avatar.user_data.config)
        resolve()
      })
      .catch(err => {
        console.log(err)
        reject()
      })
    })
  },
  logout (context) {
    // notify server user is logging out
    return new Promise((resolve, reject) => {
      this.$axios.$post('/rest-auth/logout/')
      .then(response => {
        console.log(response)
        resolve()
      })
      .catch(err => {
        console.error(err)
        reject()
      })
      .finally(() => {
        context.commit(SET_TOKEN, null)
      })
    })
  },
  saveConfig (context, config) {
    return new Promise((resolve, reject) => {
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
        resolve()
      })
      .catch(err => {
        console.log(err.response.data)
        reject()
      })
    })
  }
}
