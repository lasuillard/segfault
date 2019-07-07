<template>
  <header>
    <h1>SegFault</h1>
    <p>Test page</p>
    <nuxt-link to="/avatars">
      Go get some data
    </nuxt-link>
  </header>
</template>

<script>
export default {
  head() {
    return {
      title: "SegFault"
    }
  }
}
</script>
