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
            :error-messages="veeErrors.collect('credentials.email')"
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
            :error-messages="veeErrors.collect('credentials.password1')"
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
            :error-messages="veeErrors.collect('credentials.password2')"
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

const URL_REGISTRATION = '/rest-auth/registration/'

export default {
  asyncData (context) {
    /*
      load serverside validation info by OPTIONS request
    */
    return context.$axios.$options(URL_REGISTRATION)
    .then(response => {
      return { ssv: response.actions }
    })
    .catch(err => console.log(err.response))
  },
  data: () => ({
    ssv: {},
    credentials: {
      email: null,
      password1: null,
      password2: null
    }
  }),
  computed: {
    isFormFilled () {
      return Object.values(this.credentials).every(field => Boolean(field))
    }
  },
  methods: {
    signUp () {
      this.$axios.$post(URL_REGISTRATION, {
        ...this.credentials
      })
      .then(response => {
        
      })
      .catch(err => {

      })
    }
  }
}
</script>
