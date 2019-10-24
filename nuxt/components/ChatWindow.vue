<!--메시지 파싱 구현하십시오-->
<template>
  <v-card>
    <div class="container" style="max-width: 90%;">
      <p>{{ messages }}</p>
      <v-text-field
        v-model="message"
        :append-outer-icon="'mdi-send'"
        clear-icon="mdi-close-circle"
        clearable
        label="Message"
        type="text"
        @click:append-outer="send"
        @click:clear="clearMessage"
      ></v-text-field>
    </div>
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
    clearMessage () {
      this.message = ''
    },
  }
}
</script>