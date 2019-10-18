<template>
  <div>
    <p>Answer for fragment</p>
    
      <v-divider></v-divider>
    <editor v-model="content"/>
      <v-divider></v-divider>

    <v-btn @click="post" dark color="primary">Submit</v-btn>
  </div>
</template>

<script>

const BASE_URL_ANSWER = '/api/v1/answer'

import { Editor, Viewer } from '@toast-ui/vue-editor'
import 'tui-editor/dist/tui-editor.css';
import 'tui-editor/dist/tui-editor-contents.css';
import 'codemirror/lib/codemirror.css';


export default {
  components: {
    'editor': Editor,
    'viewer': Viewer
  },
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