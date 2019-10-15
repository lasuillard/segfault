<template>
  <v-card>
    <v-card-title>
      <span class="headline">Sign in</span>
    </v-card-title>
    <v-card-text>
      <v-container @keyup.enter="bindLocalLogin">
        <v-layout wrap>
          <v-flex xs12>
            <v-text-field
              v-model="credentials.email"
              v-validate="'required|email'"
              data-vv-name="credentials.email"
              data-vv-as="email"
              label="E-mail"
              :error-messages="String(veeErrors.collect('credentials.email')).split(',').join('<br/>')"
            />
          </v-flex>
          <v-flex xs12>
            <v-text-field
              v-model="credentials.password"
              v-validate="'required'"
              data-vv-name="credentials.password"
              data-vv-as="password"
              label="Password"
              type="password"
              :error-messages="String(veeErrors.collect('credentials.password')).split(',').join('<br/>')"
            />
          </v-flex>
          <v-flex class="mt-2" xs12>
            <v-layout justify-end>
              <v-btn
                @click="bindLocalLogin"
                color="primary"
                small
                text
                :disabled="veeErrors.any() || !isFormFilled"
              >
                Log in
              </v-btn>
            </v-layout>
          </v-flex>
          <v-flex xs12 class="mt-3">
            <div>
              You have no account yet? <nuxt-link :to="{ name: 'sign' }">join us</nuxt-link><br/>
              Or you can try...
              <v-btn @click="isExpanded = !isExpanded" x-small icon>
                <v-icon>{{ isExpanded ? 'keyboard_arrow_up' : 'keyboard_arrow_down' }}</v-icon>
              </v-btn>
            </div>
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
      email: null,
      password: null
    },
    socialLogins: [
      // static images at /static folder
      {
        provider: 'naver',
        displayName: 'Naver',
        image: '/static/Log in with NAVER_Icon_Green.png',
      },
      {
        provider: 'kakao',
        displayName: 'Kakao',
        image: '/static/kakaolink_btn_small.png'
      },
      {
        provider: 'google',
        displayName: 'Google',
        image: '/static/g-logo.png'
      }
    ]
  }),
  computed: {
    isFormFilled: function () {
      return Object.values(this.credentials).every(field => Boolean(field)) || false
    },
  },
  methods: {
    bindLocalLogin () {
      /*
        to bind various keyup and click events referencing local login
      */
      if (this.veeErrors.any() || !this.isFormFilled)
        return
        
      this.localLogin(this.credentials)
      .then(ok => {
        this.isExpanded = false
      })
      .catch(error => {
        if (error.response) {
          let feedback = error.response.data
          for (var key of Object.keys(feedback)) {
            if (this.credentials.hasOwnProperty(key)) {
              Array(feedback[key]).map(msg => {
                this.veeErrors.add({
                  field: `credentials.${key}`,
                  msg: msg,
                })
              })
            }
            else {
              // handle unhandled errors to be attached to password field
              this.veeErrors.add({
                field: 'credentials.password',
                msg: feedback[key]
              })
            }
          }
        }
        else if (error.request) {
          throw Error(error.request)
        }
        else {
          throw Error(error.message)
        }
      })
    },
    ...mapActions({
      localLogin: 'user/loginByLocal',
      trySocialLogin: 'user/trySocialLogin'
    })
  }

}
</script>
