<template>
  <v-card>
    WebSocket URL: <input type="text" id="wss_url" v-model="url" />
    /
    <v-button id="wss_connect" @click="establish_wss_connection">Connect</v-button><br/>
    Send(JSON): <textarea id="wss_message_json" v-model="data" />
    <v-button id="wss_send" @click="send_wss_message">Send</v-button><br/>
    <v-sheet id="ws_feedback_message_stack">
      Messages: <br/>
      <p v-for="message in messages" :key="message">{{ message }}</p>  
    </v-sheet>
  </v-card>
</template>

<script>

export default {
  data: () => ({
    url: 'ws://localhost:8000/ws/chat/312/',
    data: '{ "message": "Hello World!" }',
    websocket: null,
    messages: []
  }),
  methods: {
    establish_wss_connection () {
      let ws = this.websocket = new WebSocket(this.url)
      ws.onopen = (e) => {
        this.messages.push("Open websocket")
      }
      ws.onerror = (e) => {
        this.messages.push("Error on websocket: " + JSON.stringify(e))
      }
      ws.onclose = (e) => {
        this.messages.push("Closed websocket")
      }
      ws.onmessage = (e) => {
        this.messages.push("Messages on websocket: " + JSON.stringify(e.data))
      }
    },
    send_wss_message () {
      if (this.websocket)
        this.websocket.send(this.data)

    }
  }
}

</script>
