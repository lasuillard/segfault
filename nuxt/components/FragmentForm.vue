<template>
  <div>
    <v-text-field
      v-model="title"
      v-validate=""
      data-vv-name="title"
      data-vv-as="title"
      label="Title"
      :error-messages="String(veeErrors.collect('title')).split(',').join('<br/>')"
    ></v-text-field>

      <v-divider></v-divider>
    <editor v-model="content"/>
      <v-divider></v-divider>

    <v-combobox
      v-model="tags"
      v-validate=""
      data-vv-name="tags"
      data-vv-as="tags"
      label="Tags"
      :error-messages="String(veeErrors.collect('tags')).split(',').join('<br/>')"
      :items="quickTags"
      multiple clearable chips solo
    >
      <template v-slot:selection="{ attrs, item, select, selected }">
        <v-chip
          v-bind="attrs"
          :input-value="selected"
          close
          @click="select"
          @click:close="remove(item)"
        >
          {{ item }}
        </v-chip>
      </template>
    </v-combobox>
    <v-btn outlined color="primary" @click="post">DONE</v-btn>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
const BASE_URL_FRAGMENT = '/api/v1/fragment'

import { Editor, Viewer } from '@toast-ui/vue-editor'
import 'tui-editor/dist/tui-editor.css';
import 'tui-editor/dist/tui-editor-contents.css';
import 'codemirror/lib/codemirror.css';

export default {
  components: {
    'editor': Editor,
    'viewer': Viewer
  },
  data: () => ({
    title: '',
    content: '',
    tags: [],
    quickTags: ['Python', 'JavaScript'], // just for demo
  }),
  methods: {
    post () {
      this.$axios.$post(`${BASE_URL_FRAGMENT}/`, { 
        title: this.title,
        content: this.content,
        tags: this.tags
      })
      .then(async response => {
        this.$emit('created')
        this.title = ''
        this.content = ''
        this.tags = []
        alert('Posted new fragment')
      })
      .catch(error => {
        if (error.response) {
          let feedback = error.response.data
          for (var key of Object.keys(feedback)) {
            Array(feedback[key]).map(msg => {
              if (['title', 'content', 'tags'].includes(key)) {
                this.veeErrors.add({
                  field: key,
                  msg: msg,
                })
              }
              else {
                this.veeErrors.add({
                  field: 'content',
                  msg: feedback[key]
                })
              }
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
    removeTag (tag) {
      this.tags.splice(this.tags.indexOf(tag), 1)
      this.tags = [...this.tags]
    }
  }
}
</script>
