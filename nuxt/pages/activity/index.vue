<template>
  <v-container>

  <div id="app">
  <v-app id="inspire">
    <div>

 <v-responsive
      class="overflow-y-auto"
      max-height="400"
    >
      <v-responsive
        height="200vh"
        class="text-center pa-2"
      >
        <v-lazy
          v-model="isActive"
          :options="{
            threshold: .5
          }"
          min-height="200"
          transition="fade-transition"
        >
          <v-card
            class="mx-auto"
            max-width="336"
          >
            <v-card-title>Card title</v-card-title>
  
            <v-card-text>
              Phasellus magna. Quisque rutrum. Nunc egestas, augue at pellentesque laoreet, felis eros vehicula leo, at malesuada velit leo quis pede. Aliquam lobortis. Quisque libero metus, condimentum nec, tempor a, commodo mollis, magna.
  
              In turpis. In dui magna, posuere eget, vestibulum et, tempor auctor, justo. In turpis. Pellentesque dapibus hendrerit tortor. Ut varius tincidunt libero.
            </v-card-text>
          </v-card>
        </v-lazy>
      </v-responsive>
    </v-responsive>


     <v-bottom-navigation
      v-model="bottomNav"
    >
      <v-btn value="recent">
        <span>Recent</span>
        <v-icon>mdi-history</v-icon>
      </v-btn>
  
      <v-btn value="favorites">
        <span>Favorites</span>
        <v-icon>mdi-heart</v-icon>
      </v-btn>
  
      <v-btn value="nearby">
        <span>Nearby</span>
        <v-icon>mdi-map-marker</v-icon>
      </v-btn>
    </v-bottom-navigation>

    </div>
  </v-app>
</div>


  </v-container>
</template>

<script>

import { messaging } from '~/plugins/firebase.js'

export default {
  data: function() {
    return {
      colors: [
        'primary',
        'secondary',
        'red',
      ],
      items: [{
        title: "nginx 질문",
        name: "adele",
        avatar: 'https://cdn.vuetifyjs.com/images/lists/1.jpg',
        contents: "ajdskfla;jskdf333333333333333333333333333333333333333l;ajskdl;f" ,
      },
      {
        title: "도커 질문입니다!",
        name: "dave",
        avatar: 'https://cdn.vuetifyjs.com/images/lists/2.jpg',
        contents: "ajdskfla;jskdfl;ajskdl;f" ,
      },
     {
      title:"웹 소켓 질문이에요!" ,
      name: "Mike",
       avatar: 'https://cdn.vuetifyjs.com/images/lists/3.jpg',
       contents: "ajdskfla;jskdfl;ajskdl;f" ,
      }],
      links: [
      'Home',
      'About Us',
      'Dev Team',
      'Services',
      'Twitter',
      'Contact Us',
    ],
      ranking: [{
        tagName: '인공지능',
        rank: 1,
        numberQ: 23,
      },{
        tagName: 'JavaScript',
        rank: 2,
        numberQ: 22,
      }],
      hideDelimiters: true,
      cycle: true,
      height: 300,
      cardWidth: 450,
      cardHeight: 600,
      divider: true, inset: true,
    }
  },
  computed: {
    timeLable: function() {
      var time = new Date();
      return time.getHours()+':'+time.getMinutes()+':'+time.getSeconds()+' 에 동기화 됨'
    },
  },
  methods: {

  },
  created () {
    // FCM 메시지 설정 코드
    messaging.requestPermission()
        .then(function(){
            console.log('메세징 권한 획득');
            return messaging.getToken();
        })
        .then(function(token){
            console.log('fcm token: ', token);
            //// 백그라운드 작업 예시
            // $.ajax({
            //     type: "POST",
            //     url: "/main/updateToken",
            //     data: token,
            //     dataType: "TEXT",
            //     success: function(text){
            //         console.log('전송성공');
            //     },
            //     error: function(xhr, status, error){
            //         console.log(error);
            //     }
            // });
        })
        .catch(function(e){
            console.log('메세징 권한 획득 중 에러', e);
        });
  },
}

</script>
