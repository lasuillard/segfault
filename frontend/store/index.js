import { LOAD_CONFIG, CHANGE_CONFIG } from './mutation-types'

/*
  index store is to maintain state of web application settings
  
  *** no sensetive informations should be stored here ***

*/

export const state = () => ({
  theme: 'light'
})

export const getters = {
  getThemeObj: (state) => {
    return {
      [state.theme]: true
    }
  }
}

export const mutations = {
  [LOAD_CONFIG]: (state, payload) => {
    for (var key in state) {
      state[key] = payload[key] || null
    }
  },
  [CHANGE_CONFIG]: (state, { key, value }) => {
    if (Object.keys(state).includes(key)) {
      state[key] = value
    } else {
      console.error(`There's no config with key ${key}`)
    }
  }
}

export const actions = {
  loadConfig(context) {
    /*
      loads user settings from browser local stroage
    */
    try {
      let config = JSON.parse(localStorage.getItem('config'))
      if (!Boolean(config))
        return
      
      context.commit(LOAD_CONFIG, config)
    } catch(e) {
      console.error(e)
      // failed to parse JSON
    }
  },
  saveConfig({ state }) {
    localStorage.setItem('config', JSON.stringify({
      theme: state.theme
    }))
  },
  resetConfig(context) {
    context.commit(CHANGE_CONFIG, { key: 'theme', value: 'light' })
  }
}