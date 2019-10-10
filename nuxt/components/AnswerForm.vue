<template>
  <div style="border: 1px dotted black;">
    <p>Post new answer for fragment</p>
    <v-textarea
      v-model="content"
      v-validate="'required'"
      data-vv-name="content"
      data-vv-as="answer"
      label="Answer"
      :error-messages="String(veeErrors.collect('content')).split(',').join('<br/>')"
    ></v-textarea>
    <v-btn @click="post">Post new answer</v-btn>
  </div>
</template>

<script>

const BASE_URL_ANSWER = '/api/v1/answer'

export default {
  props: {
    target: {
      type: Number,
      required: true
    }
  },
  data: () => ({
    content: null,
  }),
  methods: {
    post () {
      this.$axios.$post(`${BASE_URL_ANSWER}/`, { 
        target: this.target,
        content: this.content
      })
      .then(response => {
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