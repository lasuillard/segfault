<template>
  <div>
      <!--h1>Activity</h1>
      Profile: {{ profile }}
      <hr/-->

      <!--notification-window></notification-window-->

      <hr/>

      <h2>Post new fragment</h2>
      <fragment-form @created="load"></fragment-form>
      <br/>
      <hr/>

      My Recent Fragments: {{ recentFragments }}

      <hr/>

      Related Fragments (Tagged with my latest fragment's tags for now):
      {{ relatedFragments }}

  </div>  
</template>

<script>
import NotificationWindow from '~/components/NotificationWindow.vue'
import FragmentForm from '~/components/FragmentForm.vue'
import { mapGetters } from 'vuex'

export default {
  components: {
    'notification-window': NotificationWindow,
    'fragment-form': FragmentForm,

  },
  data: () => ({
    recentFragments: null,
    relatedFragments: null,
    reactionsOnMyContents: null
  }),
  computed: {
    ...mapGetters({
      profile: 'user/getProfile',
      isLoggedIn: 'user/isLoggedIn'
    })
  },
  methods: {
    async load () {
      this.recentFragments = await this.$axios.$get(`/api/v1/fragment?avatar=${ this.profile.avatar.pk }`)
      var recentTags = []
      for (var f of this.recentFragments.results) {
        recentTags = recentTags.concat(f.tags)
      }
      recentTags = Array.from(new Set(recentTags.map(t => t.name)))
      this.relatedFragments = await this.$axios.$get(`/api/v1/fragment?tags=${ recentTags.join(',') }`)
    }
  },
  async created () {
    if (!this.isLoggedIn)
      return

    await this.load()
  },
  beforeRouteEnter (to, from, next) {
    next(vm => {
      if (!vm.$store.getters['user/isLoggedIn']) {
        alert('You need to login')
        vm.$router.replace({ name: 'index' })
        next(false)
      }
      else
        next(true)
    })
  }
}
</script>

<style>

</style>
