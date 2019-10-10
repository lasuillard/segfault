<template>
  <div style="border: 1px dotted black;">
    <p>Post new comment for commentable object</p>
    <v-textarea
      v-model="content"
      v-validate="'required'"
      data-vv-name="content"
      data-vv-as="comment"
      label="Comment"
      :error-messages="String(veeErrors.collect('content')).split(',').join('<br/>')"
    ></v-textarea>
    <v-btn @click="post">Post new comment</v-btn>
  </div>
</template>

<script>

const BASE_URL_COMMENT = '/api/v1/comment'

export default {
  props: {
    target: {
      type: Number,
      required: true
    }
  },
  data: () => ({
    content: ''
  }),
  methods: {
    post () {
      this.$axios.$post(`${BASE_URL_COMMENT}/`, { 
        target: this.target,
        content: this.content
      })
      .then(async response => {
        this.$emit('created')
      })
      .catch(error => {
        if (error.response) {
          let feedback = error.response.data
          for (var key of Object.keys(feedback)) {
            Array(feedback[key]).map(msg => {
              this.veeErrors.add({
                field: 'content',
                msg: msg,
              })
            })
          }
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
