<template>
  <v-container fluid>
    <v-flex xs12>
      <v-layout align-center justify-center fill-height>
        <p>Processing login... please wait</p>
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
      _callback: 'user/finishSocialLogin'
    })
  },
  created () {
    this._callback({ ...this.$route.query })
    .then(ok => {
      this.$router.replace({ name: 'index' })
    })
    .catch(error => {
      throw Error(error)
    })
  }
}
</script>
