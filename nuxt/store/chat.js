/*
** notification is receive-only web socket
*/
import Vue from 'vue'

       const JOIN        = 'JOIN'
export const LEAVE       = 'LEAVE'
export const LOG         = 'LOG'
export const ADD_HANDLER = 'ADD_HANDLER'

// !! HARD CODED URL !!
export const BASE_URL_WEBSOCKET_CHAT = process.env.NODE_ENV === 'production' ? 'ws://capstone-project-segfault.herokuapp.com/ws/chat' : 'ws://localhost:8000/ws/chat'


export const state = () => ({
  rooms: {
    /*
    'null': {
      ws: null,
      handlers: [() => {}, ],
      messages: [],
    }
    */
  }
})

export const getters = {
  isRoomJoined: (state) => (roomId) => {
    return state.rooms.hasOwnProperty(roomId)
  },
  getRooms: (state) => {
    return Object.keys(state.rooms)
  },
  getStatus: (state) => (roomId) => {
    let room = state.rooms.hasOwnProperty(roomId) ? state.rooms[roomId] : null
    return room ? room.ws.readyState : WebSocket.CONNECTING
  },
  getMessages: (state) => (roomId) => {
    let room = state.rooms.hasOwnProperty(roomId) ? state.rooms[roomId] : null
    return room ? room.messages : []
  }
}

export const mutations = {
  [JOIN]: (state, payload) => {
    let { roomId, token } = payload
    let room = state.rooms.hasOwnProperty(roomId) ? state.rooms[room] : null
    if (!room) {
      // open fresh websocket connection
      Vue.set(state.rooms, roomId, {
        ws: new WebSocket(`${BASE_URL_WEBSOCKET_CHAT}/${roomId}/`, ['access_token', token]),
        handlers: [() => {}, ],
        messages: []
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
      room.ws.close()
      Vue.delete(state.rooms, roomId)
    }
  },
  [LOG]: (state, { roomId, obj }) => {
    let room = state.rooms.hasOwnProperty(roomId) ? state.rooms[roomId] : null
    if (room) {
      room.messages.push(obj)
    }
  },
  [ADD_HANDLER]: (state, { roomId, handler, force_add }) => {
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
    if (room && (force_add === true || room.handlers.findIndex(f => f == handler) === (-1))) {
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
    ws.onopen = (ev) => { 
      let obj = { type: 'open', event: ev }
      context.commit(LOG, { roomId: roomId, obj: obj })
      for (var handler of room.handlers)
        handler(obj)
    }

    // when disconnected by user or server
    ws.onclose = (ev) => {
      let obj = { type: 'close', event: ev }
      context.commit(LOG, { roomId: roomId, obj: obj })
      for (var handler of room.handlers)
        handler(obj)
    }

    // error handling
    ws.onerror = (ev) => {
      let obj = { type: 'error', event: ev }
      context.commit(LOG, { roomId: roomId, obj: obj })
      for (var handler of room.handlers)
        handler(obj)
    }

    // message handling
    ws.onmessage = (ev) => {
      let obj = { type: 'message', event: ev, data: ev.data }
      context.commit(LOG, { roomId: roomId, obj: obj })
      for (var handler of room.handlers)
        handler(obj)
    }
  },
  leaveRoom (context, roomId) {
    context.commit(LEAVE, roomId)
  },
  sendMessage (context, { roomId, message }) {
    let ws = context.state.rooms.hasOwnProperty(roomId) ? context.state.rooms[roomId].ws : null
    if (ws) {
      ws.send(JSON.stringify({
        'content': message
      }))
    }
  },
}
