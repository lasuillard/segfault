<template>
  <v-container>

  <div id="app">
  <v-app id="inspire">
    <div>
      <v-carousel
       :hide-delimiters="hideDelimiters"
       :cycle="cycle"
       :height="height"
                 >
      <v-carousel-item
        v-for="(color, i) in colors"
        :key="color"
      >
        <v-sheet
          :color="color"
          height="100%"
          tile
        >
          <v-row
            class="fill-height"
            align="center"
            justify="center"
          >
            <div class="display-3">SegFault {{ i + 1 }}</div>
          </v-row>
        </v-sheet>
      </v-carousel-item>
    </v-carousel>

    <div style="margin-bottom: 60px; margin-top: 60px">
     <v-row>

     <v-card class="mx-auto" :flat="false" :height="cardHeight" :outlined="ture" :width="350" :align="center">
       <v-card-title class="display-1">SegFault?</v-card-title>
       <v-subheader>SegFault는 우리를 어디로 이끄는가? </v-subheader>
       <v-card-text class="caption"> 
          현저하게 원대하고, 무한한 봄바람이다. 그들의 꽃 불러 주는 만천하의 눈이 못할 붙잡아 싹이 부패뿐이다. 대한 뛰노는 이것이야말로 봄날의 인생의 우리 뿐이다. 속잎나고, 곳으로 모래뿐일 구할 그들의 이상, 무한한 몸이 미인을 운다.

        영원히 풀이 그들은 보내는 싶이 작고 관현악이며, 기쁘며, 천자만홍이 철환하였는가? 방황하였으며, 그러므로 긴지라 때문이다. 영락과 싶이 듣기만 열락의 있으며, 인간의 아름다우냐? 충분히 보는 피에 봄바람을 그들의 황금시대의 이상 가슴이 이것이다. 그들은 얼음에 있는 싸인 지혜는 속에서 봄바람이다. 가는 이 피고 우는 두손을 바이며, 열락의 철환하였는가?

        눈에 지혜는 그들의 고동을 그러므로 능히 힘있다. 대고, 것이다.보라, 청춘 것이다. 우리의 용기가 동산에는 불어 얼마나 그들에게 내는 하는 운다. 위하여, 설레는 가는 실로 역사를 것이다. 새가 미인을 못하다 넣는 가는 사라지지 반짝이는 그리하였는가?
        </v-card-text>
     </v-card>

     <v-card class="mx-auto" :flat="false" :height="cardHeight" :outlined="ture" :width="350" :align="center">
       <v-card-title class="display-1">Interest Fragments</v-card-title>
       <v-col>
         <v-list three-line>
           <template v-for="item in items">
             <v-list-item :key="item.title">
             <v-list-item-avatar>
              <v-img :src="item.avatar"></v-img>
            </v-list-item-avatar>

            <v-list-item-content>
              <v-list-item-title v-html="item.title"></v-list-item-title>
              <v-list-item-subtitle v-html="item.contents"></v-list-item-subtitle>
            </v-list-item-content>
           </v-list-item>

           <v-divider v-if="divider" :key="item" :inset="inset"></v-divider>
           </template>
         </v-list>
        </v-col>
      <v-col align="right">
        <p style="font-size: 9px; color: #bfbfbf;">{{timeLable}}</p>
      </v-col>
      
      <v-btn text color="primary" :to="{ name: 'fragment' }">View more..</v-btn>
     </v-card>

     <v-card class="mx-auto" :flat="false" :height="cardHeight" :outlined="ture" :width="cardWidth" :align="center">
       <v-card-title class="display-1">Fragment Distribution</v-card-title>
       <v-card-text>Recent 1 week, Top 10</v-card-text>
       <v-col>
         <v-list three-line>
           <template v-for="rank in ranking">
             <v-list-item :key="rank.tagName">
            <v-list-item-content>
              <v-list-item-title v-html="rank.tagName" class="headline"></v-list-item-title>
              <v-list-item-subtitle>
                <p>{{rank.numberQ}} of Fragment existed</p>
              </v-list-item-subtitle>
            </v-list-item-content>

           </v-list-item>
           <v-divider v-if="divider" :key="rank"></v-divider>
           </template>
         </v-list>
      </v-col>
      <v-btn text color="primary" href="">View more</v-btn>
     </v-card>

       </v-row>
      </div>
     <div>
     <v-footer color="grey darken-4" padless>
           <v-row
        justify="center"
        no-gutters
      >
        <v-btn
          v-for="link in links"
          :key="link"
          color="white"
          text
          rounded
          class="my-2"
        >
          {{ link }}
        </v-btn>
       </v-row>
       </v-footer>
      </div>
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
