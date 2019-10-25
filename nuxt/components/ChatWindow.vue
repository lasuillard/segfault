<template>
  <v-card>
    <div class="container" style="max-width: 90%;">
      <v-card class="scroll" height="500">
        {{ messages }}
      </v-card>
      <v-text-field
        v-model="input"
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
        message: this.message
      })
      this.input='' //전송 후 입력 폼 초기화
    },
    clearMessage () {
      this.input = '' //입력 폼 초기화
    },
  }
}
</script>
<style>
  .scroll {
    overflow-y: auto;
  }
</style>