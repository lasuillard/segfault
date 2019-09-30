/*
** notification is receive-only web socket
*/

const CONNECT = 'CONNECT'
const SET_STATUS = 'SET_STATUS'
export const ADD_HANDLER = 'ADD_HANDLER'

const POSSIBLE_STATUS =[WebSocket.CONNECTING, WebSocket.OPEN, WebSocket.CLOSING, WebSocket.CLOSED]

// !! HARD CODED URL !!
export const URL_WEBSOCKET_NOTIFICATION = 'ws://localhost:80/ws/notification/'


export const state = () => ({
  ws: null,
  status: WebSocket.CLOSED,
  handlers: [],
})

export const getters = {
  getStatus: (state) => {
    return state.ws ? state.ws.readyState : WebSocket.CONNECTING
  },
}

export const mutations = {
  [CONNECT]: (state, token) => {
    state.ws = new WebSocket(URL_WEBSOCKET_NOTIFICATION, ['access_token', token])
  },
  [SET_STATUS]: (state, newStatus) => {
    if (POSSIBLE_STATUS.includes(newStatus))
      state.status = newStatus
    else
      throw Error(`Unavailable status ${newStatus} received`)
  },
  [ADD_HANDLER]: (state, handler) => {
    /*
    ** adds a handler for notification message
    ** handler will be given an object like:
    ** {
    **   type: 'message' or 'error'
    **   event: Object
    ** }
    */
    state.handlers.push(handler)
  }
}

export const actions = {
  connect (context) {
    if (!context.rootGetters['user/isLoggedIn'])
      return

    context.commit(CONNECT, context.rootState.user.token)
    let ws = context.state.ws

    // status monitoring
    context.commit(SET_STATUS, WebSocket.CONNECTING)
    ws.onopen  = (ev) => { context.commit(SET_STATUS, WebSocket.OPEN) }
    ws.onclose = (ev) => { context.commit(SET_STATUS, WebSocket.CLOSED) }

    // error handling
    ws.onerror = (ev) => {
      for (handler of context.state.handlers)
        handler({ type: 'error', event: ev })
    }

    // message handling
    ws.onmessage = (ev) => {
      for (handler of context.state.handlers)
        handler({ type: 'message', event: ev })
    }
  },
}
