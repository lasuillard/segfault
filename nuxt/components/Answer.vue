<template>
  <div>
    <div style="border: 5px solid green;" class="ma-3">
      <template v-if="isLoaded">
        <!--Answer/{{ answer.pk }}/rawData: {{ JSON.stringify(rawData) }}<br/-->
        <div style="border: 2px solid gray;" class="ma-3">
          avatar : {{answer.avatar.profile_image}} User ; {{answer.avatar.display_name}}
        <v-divider/>
        <viewer :value="answer.content"> </viewer><br/>
        </div>
        Comments about this answer:<br/>
        
        <comment
          v-for="comment in rawData.comments"
          :key="comment.pk"
          :target="answer.pk"
          :comment="comment"
          @update="load"
          @delete="load"
        ></comment>
        <comment-form :target="rawData.pk" @created="load"></comment-form>
        <vote :votes="rawData.votes"></vote>
        <vote-form :target="rawData.pk" @created="load"></vote-form>
        <v-btn v-if="isOwned" @click="del">Delete this answer</v-btn>
      </template>
    </div>
  </div>
</template>

<script>
import Comment from './Comment.vue'
import CommentForm from '~/components/CommentForm.vue'
import Vote from '~/components/Vote.vue'
import VoteForm from '~/components/VoteForm.vue'

import { Editor, Viewer } from '@toast-ui/vue-editor'
import 'tui-editor/dist/tui-editor.css';
import 'tui-editor/dist/tui-editor-contents.css';
import 'codemirror/lib/codemirror.css';


const BASE_URL_ANSWER = '/api/v1/answer'

export default {
  components: {
    'comment': Comment,
    'comment-form': CommentForm,
    'vote': Vote,
    'vote-form': VoteForm,
    'editor': Editor,
    'viewer': Viewer
  },
  props: {
    target: { // parent fragment id this answer resides in
      type: Number,
      required: true
    },
    answer: { // primary key and extra informations
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
      return this.rawData && this.rawData.hasOwnProperty('comments')
    },
    isOwned: function () {
      let profile = this.$store.getters['user/getProfile']
      return profile.avatar.hasOwnProperty('pk') && profile.avatar.pk == this.rawData.avatar.pk
    }
  },
  methods: {
    async load () {
      this.rawData = await this.$axios.$get(`${BASE_URL_ANSWER}/${this.answer.pk}`)
    },
    patch () {
      this.$axios.$patch(`${BASE_URL_ANSWER}/${this.answer.pk}/`, {
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
      this.$axios.$delete(`${BASE_URL_ANSWER}/${this.answer.pk}/`)
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
