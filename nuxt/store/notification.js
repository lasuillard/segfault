/*
** notification is receive-only web socket
*/

const CONNECT = 'CONNECT'
export const ADD_HANDLER = 'ADD_HANDLER'

// !! HARD CODED URL !!
export const URL_WEBSOCKET_NOTIFICATION = 'ws://localhost:8000/ws/notification/'


export const state = () => ({
  ws: null,
  handlers: [() => {}, ],
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
  [ADD_HANDLER]: (state, { handler, force_add }) => {
    /*
    ** adds a handler for notification message
    ** handler will be given an object like:
    ** {
    **   type : 'open', 'close', 'error', 'message'
    **   event: Object
    **   data : event.data
    ** }
    */
    if (force_add === true
      || state.handlers.findIndex(f => f == handler) === (-1)) {
      state.handlers.push(handler)
    }
  }
}

export const actions = {
  connect (context) {
    if (!context.rootGetters['user/isLoggedIn'])
      return

    context.commit(CONNECT, context.rootState.user.token)
    let ws = context.state.ws

    // on connection established
    ws.onopen  = (ev) => {
      for (var handler of context.state.handlers)
        handler({ type: 'open', event: ev, data: ev.data })
    }

    // when connection completely closed (by client or server whatever)
    ws.onclose = (ev) => {
      for (var handler of context.state.handlers)
        handler({ type: 'close', event: ev, data: ev.data })
    }

    // error handling
    ws.onerror = (ev) => {
      for (var handler of context.state.handlers)
        handler({ type: 'error', event: ev, data: ev.data })
    }

    // message handling
    ws.onmessage = (ev) => {
      for (var handler of context.state.handlers)
        handler({ type: 'message', event: ev, data: ev.data })
    }
  },
}
