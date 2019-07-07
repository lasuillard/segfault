<template>
  <main>
    <h2>Avatars</h2>
    <template v-for="avatar in avatars">
      <nuxt-link :key="avatar.user" :to="{ name: 'avatars-id', params: { id: avatar.id } }">
        <avatar-card :avatar="avatar"/>
      </nuxt-link>
    </template>
  </main>
</template>

<script>
import AvatarCard from '~/components/AvatarCard.vue'

export default {
  head() {
    return {
      title: 'Avatar list'
    }
  },
  components: {
    AvatarCard
  },
  async asyncData({ $axios, params }) {
    try {
      let avatars = await $axios.$get('/avatars/')
      return { avatars }
    } 
    catch(e) {
      return { avatars: [] }
    }
  },
  data() {
    return {
      avatars: []
    }
  }
}
</script>
