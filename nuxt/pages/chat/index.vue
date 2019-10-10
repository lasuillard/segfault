<template>
  <div>
    rawData: {{ rawData }}
    <v-btn @click="load">Load More</v-btn>
    <template v-if="isLoaded">
      <div>
        Rooms:<br/>
        <template v-for="room in availableRooms">
          <div :key="room.pk">
            {{ room.name }}
            <template v-if="!isRoomJoined(room.pk)">
              <v-btn @click="join(room.pk)">Join this room</v-btn>
            </template>
            <template v-else>
              <v-btn @click="leave(room.pk)">Leave this room</v-btn>
            </template>
          </div>
        </template>
      </div>
    </template>
    <div>
      <chat-window 
        v-for="room in rooms"
        :key="room"
        :room="parseInt(room)"
      ></chat-window>
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import ChatWindow from '~/components/ChatWindow.vue'
import { mapGetters, mapMutations, mapActions } from 'vuex'
import { ADD_HANDLER } from '~/store/chat'

const BASE_URL_ROOM = '/api/v1/room'

export default {
  components: {
    'chat-window': ChatWindow
  },
  data: () => ({
    rawData: null,
    availableRooms: [],
    endOfContent: false,
  }),
  async asyncData ({ $axios }) {
    return $axios.$get(`${BASE_URL_ROOM}`)
    .then(response => {
      return {
        rawData: response,
        availableRooms: response.results
      }
    })
  },
  computed: {
    ...mapGetters({
      rooms: 'chat/getRooms',
      isRoomJoined: 'chat/isRoomJoined', 
      isLoggedIn: 'user/isLoggedIn',
    }),
    isLoaded: function () {
      // key to check is up to what kind of rendering should be delayed
      return this.rawData && this.rawData.hasOwnProperty('count')
    },
  },
  methods: {
    ...mapMutations({
      addHandler: `chat/${ADD_HANDLER}`
    }),
    ...mapActions({
      _join: 'chat/joinRoom',
      leave: 'chat/leaveRoom',
    }),
    async load () {
      if (this.endOfContent)
        return

      if (this.rawData) {
        this.rawData = await this.$axios.$get(this.rawData.next)
        this.availableRooms = this.availableRooms.concat(this.rawData.results)
      }
    },
    join (roomId) {
      if (this.isLoggedIn && !this.isRoomJoined(roomId)) {
        this._join(roomId)
      }
      else {
        alert('You should login to use chat service.')
      }
    },
  }
}
</script>