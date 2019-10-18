<template>
  <div>
    <v-card
      max-width="1500"
      class="mx-auto"
    >
  
      <v-list three-line>
        <template v-for="room in availableRooms">
          <v-subheader
            v-if="room.pk"
            :key="room.pk"
            v-text="room.name"
          ></v-subheader>
  
          <v-divider
            v-else-if="true"
            :key="room.pk"
            :inset="true"
          ></v-divider>
  
          <v-list-item
            v-else
            :key="room.pk"
            @click="join(room.pk)"
          >
            <v-list-item-avatar>
              <!--v-img :src="item.avatar"> 여기에 유저 이미지 </v-img-->
            </v-list-item-avatar>
  
            <v-list-item-content>
              <v-list-item-title v-html="room.name"></v-list-item-title>
              <!--v-list-item-subtitle v-html="item.subtitle"> 여기에 내용 </v-list-item-subtitle-->
            </v-list-item-content>
            <v-btn @click="leave(room.pk)" color="pink">Leave</v-btn>
          </v-list-item>
        </template>
      </v-list>
    </v-card>
    <v-btn
       class="mx-2"
       color="primary"
       dark
       absolute
       bottom
       right
       fab
       large
       @click="load"
      >
       <v-icon>mdi-magnify</v-icon>
   </v-btn>
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