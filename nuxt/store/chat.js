/*
** notification is receive-only web socket
*/
import Vue from 'vue'

const JOIN = 'JOIN'
export const LEAVE = 'LEAVE'
export const ADD_HANDLER = 'ADD_HANDLER'

// !! HARD CODED URL !!
export const BASE_URL_WEBSOCKET_CHAT = 'ws://localhost:8000/ws/chat'


export const state = () => ({
  rooms: {
    'null': {
      ws: null,
      handlers: [() => {}]
    }
  }
})

export const getters = {
  getStatus: (state) => (roomId) => {
    let room = state.rooms.hasOwnProperty(roomId) ? state.rooms[roomId] : null
    return room ? room.ws.readyState : WebSocket.CONNECTING
  },
}

export const mutations = {
  [JOIN]: (state, payload) => {
    let { roomId, token } = payload
    let room = state.rooms.hasOwnProperty(roomId) ? state.rooms[room] : null
    if (!room) {
      // open fresh websocket connection
      Vue.set(state.rooms, roomId, {
        ws: new WebSocket(`${BASE_URL_WEBSOCKET_CHAT}/${roomId}/`, ['access_token', token]),
        handlers: [() => {}, ]
      })
    }
    else if (room.ws.readyState == WebSocket.OPEN) {
      // already joined room
      throw Error('You have already joined room: ' + roomId)
    }
    else {
      // retry for connection
      state.rooms[roomId].ws = new WebSocket(`${BASE_URL_WEBSOCKET_CHAT}/${room}/`, ['access_token', token])
    }
  },
  [LEAVE]: (state, roomId) => {
    let room = state.rooms.hasOwnProperty(roomId) ? state.rooms[roomId] : null
    if (room) {
      room.ws.disconnect()
      Vue.delete(state.rooms, roomId)
    }
  },
  [ADD_HANDLER]: (state, roomId, handler, force_add=false) => {
    /*
    ** adds a handler for notification message
    ** handler will be given an object like:
    ** {
    **   type : 'open', 'close', 'error', 'message'
    **   event: Object
    **   data : event.data
    ** }
    */
   let room = state.rooms.hasOwnProperty(roomId) ? state.rooms[roomId] : null
   if (room && (force_add === true || _room.handlers.findIndex(f => f == handler) === (-1))) {
      room.handlers.push(handler)
    }
  }
}

export const actions = {
  joinRoom (context, roomId) {
    if (!context.rootGetters['user/isLoggedIn']) {
      console.log('Authenticated users can join room.')
      return
    }

    context.commit(JOIN, { roomId: roomId, token: context.rootState.user.token })
    let room = context.state.rooms.hasOwnProperty(roomId) ? context.state.rooms[roomId] : null
    if (!room) {
      console.log('Could not join room. invalid user token or internal server error.')
      return
    }

    let ws = room.ws
    // on connection open
    ws.onopen  = (ev) => { 
      for (var handler of room.handlers)
        handler({ type: 'open', event: ev, data: ev.data })
    }

    // when disconnected by user or server
    ws.onclose = (ev) => {
      for (var handler of room.handlers)
        handler({ type: 'close', event: ev, data: ev.data })
    }

    // error handling
    ws.onerror = (ev) => {
      for (var handler of room.handlers)
        handler({ type: 'error', event: ev, data: ev.data })
    }

    // message handling
    ws.onmessage = (ev) => {
      for (var handler of room.handlers)
        handler({ type: 'message', event: ev, data: ev.data })
    }
  },
  leaveRoom(context, roomId) {
    context.commit(LEAVE, roomId)
  }
}
