<template>
  <v-container>
    <v-layout justify-center>
      <h1 class="display-4 text-thin py-12">SegFault</h1>
    </v-layout>
    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>

    <v-divider class="my-6" />

    <h2 class="display-1 text-thin mb-3">Improve your code</h2>
    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.</p>
    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>

    <v-divider class="my-6" />

    <h2 class="display-1 text-thin mb-3">Question, and answer</h2>
    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
    <p>sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>

    <v-divider class="my-6" />

    <h2 class="display-1 text-thin mb-3">Learn through sharing experiences</h2>
    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
    <p>sunt in culpa qui officia deserunt mollit anim id est laborum.</p>

    <v-divider class="my-6" />


  </v-container>
</template>

<script>
import { messaging } from '~/plugins/firebase.js'

export default {
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
  }
}
</script>
