<template>

</template>

<script>
import { mapState, mapGetters, mapMutations, mapActions } from 'vuex'
import { ADD_HANDLER } from '~/store/notification'

export default {
  computed: {
    ...mapState({
      ws: state => state.notification.ws
    }),
    ...mapGetters({
      'isLoggedIn': 'user/isLoggedIn'
    })
  },
  methods: {
    ...mapMutations({
      'addHandler': `notification/${ADD_HANDLER}`
    }),
    ...mapActions({
      'connect': 'notification/connect'
    })
  },
  watch: {
    isLoggedIn (newStatus, status) {
      if (!newStatus)
        return

      this.connect()

      // DEBUG: simple echo handler
      this.addHandler(function (res) {
        console.log(res.type)
        console.log(res.event)
      })
      
    }
  }
}
</script>