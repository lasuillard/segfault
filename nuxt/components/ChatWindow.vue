<template>
  <v-card>
      {{ messages }}
      <v-divider/>
     <v-text-field v-model="input" label="Enter Message" single-line outlined></v-text-field>
     <v-btn @click="send" outlined color="primary">Send</v-btn>
  </v-card>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  props: {
    room: {
      type: Number,
      required: true
    },
    roomname: {
      type: String,
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
      _send: 'chat/sendMessage',
    }),
    send (message) {
      this._send({
        roomId: this.room,
        message: this.input
      })
    },
  }
}
</script>
