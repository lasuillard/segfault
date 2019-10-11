<template>
  <div>
    Notifications: {{ messages }}
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  computed: {
    ...mapGetters({
      messages: 'notification/getMessages'
    })
  }
}
</script>