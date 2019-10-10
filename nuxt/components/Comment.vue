<template>
  <div>
    <template v-if="isLoaded">
      <div style="border: 1px solid black;" class="ma-3">
        Comment/{{ comment.pk }}/rawData: {{ JSON.stringify(rawData) }}
      </div>
      <v-btn v-if="isOwned" @click="del">Delete this comment</v-btn>
    </template>
  </div>
</template>

<script>

const BASE_URL_COMMENT = '/api/v1/comment'

export default {
  props: {
    target: { // parent commentable object id this comment related with
      type: Number,
      required: true
    },
    comment: { // primary key and extra informations
      type: Object,
      required: true
    }
  },
  data: () => ({
    rawData: null,
    content: '',
  }),
  computed: {
    isLoaded: function () {
      // key to check is up to what kind of rendering should be delayed
      return this.rawData && this.rawData.hasOwnProperty('pk')
    },
    isOwned: function () {
      let profile = this.$store.getters['user/getProfile']
      return profile.avatar.hasOwnProperty('pk') && profile.avatar.pk == this.rawData.avatar.pk
    }
  },
  methods: {
    async load () {
      this.rawData = await this.$axios.$get(`${BASE_URL_COMMENT}/${this.comment.pk}`)
    },
    patch () {
      this.$axios.$patch(`${BASE_URL_COMMENT}/${this.comment.pk}/`, { 
        content: this.content 
      })
      .then(async response => {
        await this.load()
        this.$emit('update')
      })
      .catch(error => {
        throw Error(error)
      })
    },
    del () {
      this.$axios.$delete(`${BASE_URL_COMMENT}/${this.comment.pk}/`)
      .then(response => {
        this.$emit('delete')
      })
      .catch(error => {
        throw Error(error)
      })
    },
  },
  async created () {
    await this.load()
  },
}
</script>
