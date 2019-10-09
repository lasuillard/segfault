<template>
  <v-container fluid>
    <v-flex xs12>
      <v-layout align-center justify-center fill-height>
        <div>Verifying email... please wait</div>
      </v-layout>
    </v-flex>
  </v-container>
</template>

<script>

const URL_VERIFY_EMAIL = '/auth/registration/verify-email/'

export default {
  layout: 'empty',
  created () { 
    this.$axios.$post(URL_VERIFY_EMAIL, {
      key: this.$route.query.key
    })
    .then(response => {
      alert('Email verified.')
      this.$router.replace({ name: 'index' })
    })
    .catch(err => {
      // write error handling here
    })
  }
}
</script>
