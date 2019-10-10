<template>
  <v-container class="ma-12" fluid>
    <v-layout coulmn>
      <v-flex xs12 sm8>
        <div class="display-2 font-weight-regular">Join SegFault</div>
        <div class="title font-weight-thin">Questions make world better.</div>
        <v-form class="ma-6">
          <v-text-field 
            v-model="credentials.email"
            v-validate="'required|email'"
            data-vv-name="credentials.email"
            data-vv-as="email"
            class="mb-6"
            type="email"
            prepend-icon="mdi-email"
            label="E-mail"
            persistent-hint 
            :error-messages="String(veeErrors.collect('credentials.email')).split(',').join('<br/>')"
          />
          <v-text-field
            v-model="credentials.password1"
            v-validate="'required'"
            data-vv-name="credentials.password1"
            data-vv-as="password"
            class="mb-6"
            type="password"
            prepend-icon="mdi-key"
            label="Password"
            persistent-hint
            :error-messages="String(veeErrors.collect('credentials.password1')).split(',').join('<br/>')"
          />
          <v-text-field
            v-model="credentials.password2"
            v-validate="{
              required: true,
              confirmed: credentials.password1
            }"
            data-vv-name="credentials.password2"
            data-vv-as="password"
            class="mb-6"
            type="password"
            prepend-icon="mdi-key"
            label="Repeat Password"
            persistent-hint
            :error-messages="String(veeErrors.collect('credentials.password2')).split(',').join('<br/>')"
          />
          <v-layout justify-end>
            <v-btn
              @click="signUp"
              color="success"
              text
              :disabled="veeErrors.any() || !isFormFilled"
            >
              Create an account
            </v-btn>
          </v-layout>
        </v-form>
      </v-flex>
      <v-flex sm4 />
    </v-layout>
  </v-container>
</template>

<script>
import { mapActions } from 'vuex'

const URL_REGISTRATION = '/auth/registration/'

export default {
  data: () => ({
    credentials: {
      email: null,
      password1: null,
      password2: null
    },
  }),
  computed: {
    isFormFilled () {
      return Object.values(this.credentials).every(field => Boolean(field))
    },
  },
  methods: {
    signUp () {
      this.$axios.$post(URL_REGISTRATION, { ...this.credentials })
      .then(response => {
        alert(response.detail)
        this.$router.replace({ name: 'index' })
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
              // handle unhandled errors to be attached to password2 field
              this.veeErrors.add({
                field: 'credentials.password2',
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
    }
  }
}
</script>
