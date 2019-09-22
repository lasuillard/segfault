<template>
  <v-card>
    <h2>Debugging for Web Socket</h2>
    <div class="pa-2">
      <h3>Sockets (0:CONNECTING / 1:OPEN / 2:CLOSING / 3:CLOSED)</h3>
      <p>Notification: {{ ws_notification.readyState }}</p>
      <div v-for="(_ws_chat, i) in ws_chat" :key="_ws_chat">
        <p>Chat {{ i }} : {{ _ws_chat.readyState }}</p>
        <input style="border-bottom: 1px solid black" type="text" v-model="_text" /><br/>
      <button @click="sendChat(_ws_chat, _text)">Send</button>
      </div>
    </div>
    <hr />
    <div class="pa-2">
      <h3>Join Chat</h3>
      <input style="border-bottom: 1px solid black" type="text" v-model="_room" /><br/>
      <button @click="joinChatRoom(_room)">Join</button>
    </div>
    <hr />
    <div class="pa-2">
      <p>Logs</p>
      <p v-for="(log, i) in logs" :key="i">{{ log }}</p>
    </div>
    <hr />
    <div class="pa-2">
      <p>Messages</p>
      <p v-for="(message, i) in messages" :key="i">{{ message }}</p>
    </div>
    <hr />
    <div class="pa-2">
      <p>Errors</p>
      <p v-for="(error, i) in errors" :key="i">{{ error }}</p>
    </div>
  </v-card>
</template>

<script>

export default {
  data: () => ({
    _room: "",
    _text: "",

    ws_notification: null,
    ws_chat: [],
    logs: [],
    messages: [],
    errors: []
  }),
  created () {
    let ws = this.ws_notification = new WebSocket('ws://localhost/ws/notifcation/')
    ws.onopen = e => {
      this.logs.push('Opened socket for notification: ' + JSON.stringify(e))
    }
    ws.onmessage = e => {
      this.messages.push('Received message: ' + JSON.stringify(e.data))
    }
    ws.onerror = e => {
      this.errors.push('Error: ' + JSON.stringify(e))
    }
    ws.onclose = e => {
      this.logs.push('Closed socket for notification: ' + JSON.stringify(e))
    }
  },
  methods: {
    joinChatRoom(room) {
      let ws = new WebSocket(`ws://localhost/ws/chat/${room}/`)
      this.ws_chat.push(ws)
      ws.onopen = e => {
        this.logs.push(`Opened socket for chat room ${room}: ` + JSON.stringify(e))
      }
      ws.onmessage = e => {
        this.messages.push('Received message: ' + JSON.stringify(e.data))
      }
      ws.onerror = e => {
        this.errors.push(`Error (room:${room}): ` + JSON.stringify(e))
      }
      ws.onclose = e => {
        this.logs.push(`Closed socket for cha room ${room}: ` + JSON.stringify(e))
      }
    },
    sendChat(ws, text) {
      ws.send(JSON.stringify({ message: text }))
    }
  },
}

</script>
