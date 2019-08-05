<template>
  <h2>Processing login... please wait</h2>
</template>

<script>
export default {
  created() { this.$store.dispatch('user/finishSocialLogin', this.$route.query) }
}
</script>
