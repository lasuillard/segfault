<template>
  <v-container class="ma-12" fluid>
    <v-layout coulmn>
      <v-flex xs12 sm8>
        <div class="display-2 font-weight-regular">Join SegFault</div>
        <div class="title font-weight-thin">Questions make world better.</div>
        <v-form class="ma-6">
          <v-text-field 
            class="mb-6"
            type="email"
            prepend-icon="mdi-email"
            label="E-mail"
            persistent-hint 
            hint="Lorem ipsum"
          />
          <v-text-field
            class="mb-6"
            prepend-icon="mdi-account"
            label="Username" 
            persistent-hint 
            hint="Lorem ipsum"
          />
          <v-text-field
            class="mb-6"
            type="password"
            prepend-icon="mdi-key"
            label="Password"
            persistent-hint
            hint="Lorem ipsum"
          />
          <v-text-field
            class="mb-6"
            type="password"
            prepend-icon="mdi-key"
            label="Repeat Password"
            persistent-hint
            hint="Lorem ipsum"
          />
          <v-layout justify-end>
          <v-btn
            @click="signUp"
            color="success"
            text
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
      username: null,
      password1: null,
      password2: null
    }
  }),
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
