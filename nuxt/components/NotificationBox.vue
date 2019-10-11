<template>

</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import { ADD_HANDLER } from '~/store/notification'

export default {
  computed: {
    ...mapGetters({
      messages: 'notification/getMessages',
      isLoggedIn: 'user/isLoggedIn'
    })
  },
  methods: {
    ...mapActions({
      connect: 'notification/connect'
    })
  },
  watch: {
    isLoggedIn (newStatus, status) {
      // try connect to notificiation websocket on user login
      if (newStatus)
        this.connect()
    }
  }
}
</script>