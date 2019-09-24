import { getLoginPage } from '~/src/auth'

// defaults
export const DEFAULT_PROFILE = {
  email: '',
  avatar: {
    display_name: 'Guest',
    profile_image: '',
  }
}
export const DEFAULT_CONFIG = {
  theme: 'light'
}

// mutation-types
export const SET_TOKEN   = 'SET_TOKEN'
export const SET_PROFILE = 'SET_PROFILE'
export const SET_CONFIG  = 'SET_CONFIG'

// urls for api
const URL_LOCAL_LOGIN  = '/auth/login/'
const URL_SOCIAL_LOGIN = '/auth/o/'
const URL_LOGOUT       = '/auth/logout/'
const URL_USER_PROFILE = '/auth/user/'


export const state = () => ({
  token : null,
  profile: null,
  config: null,
})

export const getters = {
  isLoggedIn: (state) => {
    return Boolean(state.token)
  },
  getProfile: (state, getters) => {
    let profile = { ...DEFAULT_PROFILE }
    if (getters.isLoggedIn && state.profile) {
      profile = state.profile
    }
    return profile
  },
  getConfig: (state) => {
    let config = { ...DEFAULT_CONFIG }
    if (state.config) {
      config = state.config
    }
    return config
  },
  getThemeObj: (state) => {
    /*
    returns object that will be used with v-bind
    */
    if (state.config && state.config.hasOwnProperty('theme')) {
      let theme = state.config.theme
      return {
        [theme]: true
      }
    }
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
  [SET_PROFILE]: (state, profile) => {
    if (profile) {
      state.profile = profile
    }
  },
  [SET_CONFIG]: (state, config) => {
    state.config = config
  }
}

export const actions = {
  loadToken (context) {
    return new Promise((resolve, reject) => {
      /*
      this action includes redundant statements
      to support various type of storages for future
      */
      try {
        if (true) {
          let storedToken = localStorage.getItem('token')
          if (storedToken) {
            context.commit(SET_TOKEN, storedToken)
          }
          resolve(true)
        }
        else {
          throw Error('Not implemented.')
        }
      }
      catch (e) {
        return reject(e)
      }
    })
  },
  saveConfig (context, config) {
    return new Promise(async (resolve, reject) => {
      context.commit(SET_CONFIG, config)
      try {
        let result = null
        if (context.getters.isLoggedIn) {
          let avatar = context.getters.getProfile.avatar
          if (avatar.hasOwnProperty('url')) {
            result = await this.$axios.$patch(avatar.url, {
              extra_data: {
                config: context.state.config
              }
            })
          }
          else {
            throw Error('User logged in but avatar instance is invalid.')
          }
        }
        return resolve(result)
      }
      catch (e) {
        return reject(e)
      }
    })
  },
  loginByLocal (context, credentials) {
    return new Promise(async (resolve, reject) => {
      try {
        let data = await this.$axios.$post(URL_LOCAL_LOGIN, {
          email   : credentials.email,
          password: credentials.password,
        })
        let token = data.key

        if (token) {
          return context.dispatch('_afterLogin', { token: token, })
        }
        else {
          throw new Error(`Login failed with invalid key: ${token}`)
        }
      }
      catch (e) {
        return reject(e)
      }
    })
  },
  trySocialLogin (context, provider) { 
    /*
    in social login, the code is redirected to certain page(/auth/o/) as query parameter
    so the client should send this code and obtain token from server
    */
    let href = getLoginPage(provider)
    if (href) {
      window.location.href = href
    }
    else {
      throw Error(`Provider ${provider} is not defined or not supported.`)
    }
  },
  finishSocialLogin (context, rsResponse) {
    /*
    this action will pack querystring into body and send it to server to get token
    */
    return new Promise(async (resolve, reject) => {
      let { provider } = rsResponse
      delete rsResponse.provider // no need to send server, just for routing
      try {
        let data = await this.$axios.$post(`${URL_SOCIAL_LOGIN}${provider}/`, { ...rsResponse })
        let token = data.key
        if (token) {
          return context.dispatch('_afterLogin', { token: token, })
        }
        else {
          throw new Error(`Social login (${provider}) failed with invalid key: ${token}`)
        }
      }
      catch (e) {
        return reject(e)
      }
    })
  },
  _afterLogin (context, { token }) {
    /*
    load user informations (profile, config, ...)
    */
    return new Promise(async (resolve, reject) => {
      try {
        context.commit(SET_TOKEN, token)
        
        // when token is set, authorization headers will be set (see plguins/axios.js)
        let profile = await this.$axios.$get(URL_USER_PROFILE)
        context.commit(SET_PROFILE, profile)
  
        // load avatar config
        let avatar = await this.$axios.$get(profile.avatar.url)
        if (avatar.extra_data && avatar.extra_data.hasOwnProperty('config'))
          context.commit(SET_CONFIG, avatar.extra_data.config)

        return resolve(true)
      }
      catch (e) {
        return reject(e)
      }
    })
  },
  logout (context) {
    /*
    notify server user logging out
    */
    return new Promise((resolve, reject) => {
      this.$axios.$post(URL_LOGOUT)
      .then(_ => { // no interests in response
        resolve(true)
      })
      .catch(err => {
        reject(err)
      })
      .finally(() => {
        context.commit(SET_TOKEN, null)
      })
    })
  },
}
