
export const state = () => ({
  list: []
})

export const getters = {

}

export const mutations = {
  ADD: (state, message) => {
    state.list.push(message)
  },
}
