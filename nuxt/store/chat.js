/*
** notification is receive-only web socket
*/

export const JOIN = 'JOIN'
export const LEAVE = 'LEAVE'
const SET_STATUS = 'SET_STATUS'
export const ADD_HANDLER = 'ADD_HANDLER'

const POSSIBLE_STATUS =[WebSocket.CONNECTING, WebSocket.OPEN, WebSocket.CLOSING, WebSocket.CLOSED]

// !! HARD CODED URL !!
export const BASE_URL_WEBSOCKET_CHAT = 'ws://localhost:80/ws/chat'


export const state = () => ({
  rooms: {}
})

export const getters = {
  getStatus: (state, room) => {
    return state[room].ws ? state.ws[room].readyState : WebSocket.CONNECTING
  },
}

export const mutations = {
  [JOIN]: (state, room, token) => {
    if (!state.rooms.hasOwnProperty(room)) {
      state.rooms[room] = {
        ws: null,
        status: WebSocket.CONNECTING,
        handlers: []
      }
    }
    _room = state.rooms[room]
    _room.ws = new WebSocket(`${BASE_URL_WEBSOCKET_CHAT}/${room}/`, ['access_token', token])
  },
  [LEAVE]: (state, room) => {
    if (!state.rooms.hasOwnProperty(room))
      return

    _room = state.rooms[room]
    _room.status = WebSocket.CLOSING

  },
  [SET_STATUS]: (state, newStatus) => {
    if (POSSIBLE_STATUS.includes(newStatus))
      state.status = newStatus
    else
      throw Error(`Unavailable status ${newStatus} received`)
  },
  [ADD_HANDLER]: (state, room, handler) => {
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
