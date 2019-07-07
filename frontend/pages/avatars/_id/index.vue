<template>
  <main>
    <h3>Avatar of {{ avatar.display_name }}</h3>
    <avatar-card :avatar="avatar"/>
  </main>
</template>

<script>
import AvatarCard from '~/components/AvatarCard.vue'

export default {
  head() {
    return {
      title: 'Avatar detail page'
    }
  },
  components: {
    AvatarCard
  },
  async asyncData({ $axios, params }) {
    try {
      let avatar = await $axios.$get(`/avatars/${params.id}`)
      return { avatar }
    }
    catch(e) {
      return null
    }
  },
  data() {
    return {
      avatar: {
        id: (-1),
        profile_image: '',
        display_name: 'Unknown',
        introduce_message: '',
      }
    }
  }

  
}
</script>
