<template>
  <div>
    <h2>Fragment/{{ $route.params.id }}</h2>
    <p>{{ JSON.stringify(rawData) }}</p>
  </div>
</template>

<script>

const URL_FRAGMENT_DETAIL = '/api/v1/fragment'

export default {
  data: () => ({
    rawData: null,
  }),
  async created () {
    this.rawData = await this.$axios.$get(`${URL_FRAGMENT_DETAIL}/${this.$route.params.id}`)
  },
}
</script>