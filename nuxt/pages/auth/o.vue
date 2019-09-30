<template>
  <v-container fluid>
    <v-flex xs12>
      <v-layout align-center justify-center fill-height>
        <div>Processing login... please wait</div>
      </v-layout>
    </v-flex>
  </v-container>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  layout: 'empty',
  methods: {
    ...mapActions({
      _finishLogin: 'user/finishSocialLogin'
    })
  },
  created () { 
    this._finishLogin(this.$route.query)
    .then(ok => this.$router.replace({ name: 'index' }))
    .catch(err => {
      // write error handling here
    })
  }
}
</script>
