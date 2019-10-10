<template>
  <div style="border: 1px dotted black;">
    <p>Vote for votable object</p>
    <v-btn @click="post('upvote')">Upvote</v-btn>
    <v-btn @click="post('downvote')">Downvote</v-btn>
  </div>
</template>

<script>

const BASE_URL_VOTE = '/api/v1/vote'

const CHOICES = {
  'upvote': 1,
  'default': 0,
  'downvote': -1
}

export default {
  props: {
    target: {
      type: Number,
      required: true
    }
  },
  data: () => ({
    rating: null,
  }),
  methods: {
    post (choice) {
      this.$axios.$post(`${BASE_URL_VOTE}/`, { 
        target: this.target,
        rating: Object.keys(CHOICES).includes(choice) ? CHOICES[choice] : CHOICES['default']
      })
      .then(response => {
        this.$emit('created')
      })
      .catch(error => {
        if (error.response) {
          throw Error(error.response)
        }
        else if (error.request) {
          throw Error(error.request)
        }
        else {
          throw Error(error.message)
        }
      })
    },
  }  
}
</script>