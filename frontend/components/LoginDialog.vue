<template>
  <v-card>
    <v-card-title>
      <span class="headline">Sign in</span>
    </v-card-title>
    <v-card-text>
      <v-container>
        <v-layout wrap>
          <v-flex xs12>
            <v-text-field
              v-model="credentials.account"
              @keyup.enter="bindLocalLogin"
              label="Account"
              required
            />
          </v-flex>
          <v-flex xs12>
            <v-text-field
              v-model="credentials.password"
              @keyup.enter="bindLocalLogin"
              label="Password"
              type="password"
              required
            />
          </v-flex>
          <v-flex class="mt-2" xs12>
            <v-layout justify-end>
              <v-btn
                @click="bindLocalLogin"
                color="primary"
                small
                text
              >
                Log in
              </v-btn>
            </v-layout>
          </v-flex>
          <v-flex xs12 class="mt-3">
            You have no account yet? join us <nuxt-link :to="{ name: 'sign' }">here</nuxt-link>
            <br />
            Or you can try...
            <v-btn @click="isExpanded = !isExpanded" x-small icon>
              <v-icon>{{ isExpanded ? 'keyboard_arrow_up' : 'keyboard_arrow_down' }}</v-icon>
            </v-btn>
          </v-flex>
          <v-expand-transition>
            <div v-show="isExpanded" class="mt-3">
              <v-btn
                v-for="service in socialLogins"
                :key="service.provider"
                @click="trySocialLogin(service.provider)"
                class="mt-1"
                large
                block
                text
              >
                <v-layout align-center>
                <v-img :src="service.image" max-width="32px" max-height="32px" />
                <span class="ml-3">Log in with {{ service.displayName }}</span>
                </v-layout>
              </v-btn>
            </div>
          </v-expand-transition>
        </v-layout>
      </v-container>
    </v-card-text>
  </v-card>
</template>

<script>
import { mapActions } from 'vuex'

export default { 
  data: () => ({
    isExpanded: false,
    credentials: {
      account: null,
      password: null
    },
    socialLogins: [
      {
        provider: 'naver',
        displayName: 'Naver',
        image: '/Log in with NAVER_Icon_Green.png',
      },
      {
        provider: 'kakao',
        displayName: 'Kakao',
        image: '/kakaolink_btn_small.png'
      },
      {
        provider: 'google',
        displayName: 'Google',
        image: '/g-logo.png'
      }
    ]
  }),
  methods: {
    bindLocalLogin() {
      /*
        to bind various keyup and click events referencing local login
      */
      this.localLogin(this.credentials)
    },
    ...mapActions({
      localLogin: 'user/loginByLocal',
      trySocialLogin: 'user/trySocialLogin'
    })
  }

}
</script>
