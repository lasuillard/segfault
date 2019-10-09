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

export default {
  layout: 'empty',
  created () { 
    this.$store.dispatch('user/finishSocialLogin', { ...this.$route.query })
    .then(ok => {
      this.$router.replace({ name: 'index' })
    })
    .catch(error => {
      throw Error(error)
    })
  }
}
</script>
