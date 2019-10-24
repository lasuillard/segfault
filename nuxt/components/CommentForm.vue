<template>
  <div>
    <v-textarea
      v-model="content"
      v-validate="'required'"
      data-vv-name="content"
      data-vv-as="comment"
      label="Comment"
      :error-messages="String(veeErrors.collect('content')).split(',').join('<br/>')"
    ></v-textarea>
    <v-row
        align="center"
        justify="end"
      >
        <v-btn @click="post" color="primary">Post</v-btn>
      </v-row>
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
