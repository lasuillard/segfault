<template>
<div>
  <div class="ac-banner white-text col-12">
      <div class="row sub-banner">
          <div class="container" style="max-width: 70%;">
              <div class="col-sm12 col-md6 acinfo">
                  <hh class="userinfo"><b>Live Chat</b></hh>
                  <p class="userinfo subinfo" style="font-size: 16px;">Chat with other developers</p>
              </div>
              <div class="col-sm12 col-md6 sbinfo">
              </div>
          </div>
      </div>
  </div>
  <div class="container" style="max-width: 70%; min-height: 105vh !important;">
    <!--v-btn @click="load">Load More</v-btn-->
    <template v-if="isLoaded">
        <v-sheet v-for="room in availableRooms" 
        :key="room.pk" 
        class="pa-3 px-4 my-4"
        elevation="1">
         <v-row>
            <v-col cols="3" md="2" align-self="center">
              <div class="mb-2 body-1 text-center">
                {{ room.pk }}
              </div>
              <v-divider />

            </v-col>
            <v-col cols="9" md="10">
              <v-row class="mb-2" no-gutters>
                <v-col>
                  <div class="title" style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{{ room.name }}</div>
                  <div class="subtitle-1">Participant : {{ (room.user) }}</div>
                  <div calss="subtitle-1"> {{getTimeDeltaStr(room.date_created)}} </div>
                  <div class="caption">Last change : {{ room.date_modified }}</div>
                </v-col>
                  <v-col lg="2">
                    <div style="margin-bottom: 10px">
                       <v-btn @click="join(room.pk)" outlined color="blue darken-1">Enter</v-btn> 
                    </div>
                    <div>
                       <v-btn @click="leave(room.pk)" outlined color="red lighten-1">Leave </v-btn>  
                    </div>
                  </v-col>
              </v-row>
            </v-col>
          </v-row>
        </v-sheet>


        <!--template v-for="room in availableRooms">
          <div :key="room.pk">
            {{ room.name }}
            <template v-if="!isRoomJoined(room.pk)">
              <v-btn @click="join(room.pk)">Join this room</v-btn>
            </template>
            <template v-else>
              <v-btn @click="leave(room.pk)">Leave this room</v-btn>
            </template>
          </div>
        </template-->
    </template>
  </div>

  <div>
    <chat-window 
    v-for="room in rooms"
    :key="room"
    :room="parseInt(room)"
    ></chat-window>
   </div>

  <footer id="footer" class="page-footer dk">
      <div class="footer-copyright dk">
          <div class="container" style="max-width: 70%; color: rgba(255,255,255,0.8);">
          © 2019 SegFault, All rights reserved. 
          <a class="grey-text text-lighten-4 right" href="#!"></a>
          </div>
      </div>
  </footer>
</div>
</template>

<script>
import Vue from 'vue'
import ChatWindow from '~/components/ChatWindow.vue'
import { mapGetters, mapMutations, mapActions } from 'vuex'
import { ADD_HANDLER } from '~/store/chat'

const BASE_URL_ROOM = '/api/v1/room'
const BASE_URL_AVATAR = '/api/v1/avatar'

export default {
  components: {
    'chat-window': ChatWindow
  },
  data: () => ({
    rawData: null,
    availableRooms: [],
    endOfContent: false,
    userList: [],
  }),
  async asyncData ({ $axios }) {
    var uList = await $axios.$get(`${BASE_URL_AVATAR}`)    
    return $axios.$get(`${BASE_URL_ROOM}`)
    .then(response => {
      return {
        rawData: response,
        availableRooms: response.results,
        userList: uList.results, 
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
    getTimeDeltaStr(date) {
      var milliseconds = Date.now() - new Date(date)
      var seconds = Math.round(milliseconds / 1000)
      var minutes = Math.round(seconds / 60)
      if (minutes == 0)
        return `${seconds} seconds ago`
      
      var hours = Math.round(minutes / 60)
      if (hours == 0)
        return `${minutes} minutes ago`

      var days = Math.round(hours / 24)
      if (days == 0)
        return `${hours} hours ago`

      return `${days} days ago`
    },
  }
}
</script>
<style>
/* 상단 배너관련 css */
.ac-banner {
    background: linear-gradient(to bottom,#005799 0,#0076d1);
    box-shadow: 0 12px 45px -8px rgba(0,120,215,.35);
}
.sub-banner {
    padding-top: 20px;
    padding-bottom: 20px;
}
.acinfo {
    margin-top: 14px;
}
.sbinfo{
    margin-top: 14px;
}
.userinfo {
    margin-top: 0px;
    margin-bottom: 0px;
}
.midinfo {
    font-size: 15px;
}
.subinfo {
    color: #96cbed;
    margin-top: 5px;
    font-size: 13px;
}
hh {
    font-size: 2.28rem;
    line-height: 110%;
    margin: 1.52rem 0 .912rem 0;
}
</style>