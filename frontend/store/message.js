
export const state = () => ({
  list: []
})

export const mutations = {
  ADD: (state, message) => {
    state.list.push(message)
  },
}

export const getters = {
  getAll(state) {
    return state.list
  },
}
