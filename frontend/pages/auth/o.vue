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
export default {
  layout: 'empty',
  created() { this.$store.dispatch('user/finishSocialLogin', this.$route.query) }
}
</script>
