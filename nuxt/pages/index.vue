<template>

  <div id="app">
  <v-app id="inspire">
    <div>
      <header>
          <div id="index_00" class="row front-main">
              <div class="col s12 mback valign-wrapper">
                <div id="left_side" class="text-center white-text" style="width:100%;">
                    <h1 class="stretch white-text sd">SegFault</h1>
                    <p class="stretch">Innovation in development</p>
                </div>
              </div>
          </div>
      </header>
      <article>
        <div id="index_01" class="row">
          <!--왼쪽 6단-->
          <div class="col-sm-6 left" style="min-height: 105vh !important;">
            <v-container>
              <div id="left_side" class="left-text" style="width:100%;">
                  <v-card-title class="display-1">Recent Fragments</v-card-title>
                  <v-col>
                    <v-list three-line>
                      <template v-for="item in recentFragments">
                        <v-list-item :key="item.pk">
                          <v-list-item-avatar>
                            <v-img :src="item.avatar.profile_image"></v-img>
                          </v-list-item-avatar>
                          <v-list-item-content>
                            <v-list-item-title>{{ item.title }}</v-list-item-title>
                            <v-list-item-subtitle>{{ Array(item.tags.map(v => v.name)).slice(0, 2).join(', ') }}</v-list-item-subtitle>
                          </v-list-item-content>
                        </v-list-item>
                        <v-divider inset :key="`_${item.pk}`"></v-divider>
                      </template>
                    </v-list>
                    </v-col>
                  <v-col align="right">
                    <p style="font-size: 9px; color: #bfbfbf;">{{timeLable}}</p>
                  </v-col>
                  <v-btn text color="primary" :to="{ name: 'fragment' }">View more..</v-btn>
              </div>
            </v-container>
          </div>
          <!--오른쪽 6단-->
          <div class="col-sm-6 right" style="min-height: 105vh !important;">
            <v-container>
              <div id="right_side" class="white-text">
                  <v-card-title class="display-1">Popular Tags</v-card-title>
                  <v-col>
                    <v-list three-line>
                      <template v-for="tag in popularTags">
                        <v-list-item :key="tag.pk">
                          <v-list-item-content>
                            <v-list-item-title class="headline">{{ tag.name }}</v-list-item-title>
                            <v-list-item-subtitle>
                              <p>There are {{ tag.count_related_contents || 0 }} related contents</p>
                            </v-list-item-subtitle>
                          </v-list-item-content>
                        </v-list-item>
                        <v-divider inset :key="`_${tag.pk}`"></v-divider>
                      </template>
                    </v-list>
                  </v-col>
                  <v-btn text color="primary" href="">View more</v-btn>
              </div>
            </v-container>
          </div>
        </div>
      </article>
      <footer id="footer" class="page-footer dk">
          <div class="footer-copyright dk">
              <div class="container" style="max-width: 70%; color: rgba(255,255,255,0.8);">
              © 2019 SegFault, All rights reserved. 
              <a class="grey-text text-lighten-4 right" href="#!"></a>
              </div>
          </div>
      </footer>
    </div>
  </v-app>
</div>
</template>

<script>
import { messaging } from '~/plugins/firebase.js'

export default {
  data: () => ({
    colors: [
      'primary',
      'secondary',
      'red',
    ],
    recentFragments: null,
    popularTags: null,
    hideDelimiters: true,
    cycle: true,
    height: 300,
    cardWidth: 450,
    cardHeight: 600,
    links: [
      'Home',
      'About Us',
      'Dev Team',
      'Services',
      'Twitter',
      'Contact Us',
    ],
  }),
  async asyncData ({ $axios }) {
    var recentFragments = await $axios.$get('/api/v1/fragment?limit=10')
    var popularTags = await $axios.$get('/api/v1/tag?order=count_related_content')
    return {
      recentFragments: recentFragments.results,
      popularTags: popularTags.results
    }
  },
  computed: {
    timeLable: function() {
      var time = new Date()
      return 'Synchrnoized data at ' + time.getHours() + ':' + time.getMinutes() + ':' + time.getSeconds()
    },
  },
  methods: {

  },
  // created () {
  //   // FCM 메시지 설정 코드
  //   messaging.requestPermission()
  //       .then(function(){
  //           console.log('메세징 권한 획득');
  //           return messaging.getToken();
  //       })
  //       .then(function(token){
  //           console.log('fcm token: ', token);
  //           //// 백그라운드 작업 예시
  //           // $.ajax({
  //           //     type: "POST",
  //           //     url: "/main/updateToken",
  //           //     data: token,
  //           //     dataType: "TEXT",
  //           //     success: function(text){
  //           //         console.log('전송성공');
  //           //     },
  //           //     error: function(xhr, status, error){
  //           //         console.log(error);
  //           //     }
  //           // });
  //       })
  //       .catch(function(e){
  //           console.log('메세징 권한 획득 중 에러', e);
  //       });
  // }
}

</script>
<style>
.front-main { height:70vh; }
.mback {
  background-image: url('~assets/mainBack.png');
  background-size: cover;
}
.dk {
    background-color: rgb(51,51,51);
}
.sd { text-shadow: 4px 2px 2px rgb(51,51,51); }
.left { background-color: #F2F2F2; }
.right { background-color: #232838; }
.valign-wrapper {
    display: -webkit-box;
    display: -webkit-flex;
    display: -ms-flexbox;
    display: flex;
    -webkit-box-align: center;
    -webkit-align-items: center;
    -ms-flex-align: center;
    align-items: center;
}
h1 {
    font-size: 4.2rem;
    line-height: 110%;
    font-weight: 400;
    margin: 2.8rem 0 1.68rem 0;
}
p {
    font-size: 18px;
}
.white-text {
    color: #fff !important;
}
.left-text {
    color: #343434 !important;
}

</style>