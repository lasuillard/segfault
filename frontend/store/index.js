import { CHANGE_THEME } from './mutation-types'

const $app = window.$nuxt

export const state = () => ({
  theme: 'light'
})

export const getters = {
  getSupportedThemes (_) {
    return Object.keys($app.$vuetify.theme.themes)
  },
  getCurrentTheme (state) {
    return {
      [state.theme]: true
    }
  }
}

export const mutations = {
  [CHANGE_THEME]: (state, newTheme) => {
    const supportedThemes = $app.$store.getters['getSupportedThemes']
    if (supportedThemes.includes(newTheme)) {
      state.theme = newTheme
    } else {
      console.error(`Theme ${newTheme} is not supported.`)
    }
  }
}

export const actions = {

}