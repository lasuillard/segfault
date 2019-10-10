<template>
  <div>
    Room {{ room }}<br/>
    {{ messages }}
    <v-text-field v-model="input"></v-text-field>
    <v-btn @click="send">Send</v-btn>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  props: {
    room: {
      type: Number,
      required: true
    }
  },
  data: () => ({
    input: ''
  }),
  computed: {
    ...mapGetters({
      _getMessages: 'chat/getMessages'
    }),
    messages: function () {
      return this._getMessages(this.room)
    }
  },
  methods: {
    ...mapActions({
      _send: 'chat/sendMessage'
    }),
    send (message) {
      this._send({
        roomId: this.room,
        message: this.input
      })
    }
  }
}
</script>
