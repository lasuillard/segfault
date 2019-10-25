<template>
  <div>
    <template v-if="isLoaded">
      <v-card
        class="mx-auto"
        color="#FFFFFF"
        style="margin-bottom: 20px;"
      >
        <v-card-title>
            <v-list-item-avatar>
              <v-img
                class="elevation-6"
                :src="answer.avatar.profile_image"
              ></v-img>
            </v-list-item-avatar>
    
            <v-list-item-content>
              <v-list-item-title>
                <a style="font-family: Segoe UI Semibold,Segoe UI,SegoeUI; font-size: 16px; color: #0067b8;">{{answer.avatar.display_name}}</a>
                <span style="float: right;">
                  <p style="display: inline; color: #5e5e5e; font-family: Segoe UI,SegoeUI,Helvetica,Arial,sans-serif; font-size: 16px;">Created on {{ createdTime }}</p>
                </span>  
              </v-list-item-title>
            </v-list-item-content>
        </v-card-title>
    
        <v-card-text style="font-size: 15px; font-family: Segoe UI,SegoeUI,Helvetica Neue,Helvetica,Arial,sans-serif; color: #000;">
          {{answer.content}}
        </v-card-text>
    
        <v-card-actions>
          <v-list-item class="grow">
            <v-row
              align="center"
              justify="end"
            >
              <a v-if="isOwned" @click="del" style="margin-top: 20px; color: #900020">Delete this answer</a>
            </v-row>
          </v-list-item>
        </v-card-actions>
        <div class="container" style="max-width: 95%; padding-bottom: 30px">
          <p style="font-weight: 600; line-height: 24px; font-family: Segoe UI,SegoeUI,Helvetica,Arial,sans-serif;">Comments</p>
          
          <comment
            v-for="comment in rawData.comments"
            :key="comment.pk"
            :target="answer.pk"
            :comment="comment"
            @update="load"
            @delete="load"
          ></comment>
          <comment-form :target="rawData.pk" @created="load"></comment-form>
        </div>
        <!-- <vote :votes="rawData.votes"></vote>
        <vote-form :target="rawData.pk" @created="load"></vote-form> -->
      </v-card>
      <!--Answer/{{ answer.pk }}/rawData: {{ JSON.stringify(rawData) }}<br/-->
    </template>
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
import moment from 'moment'


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
    },
    createdTime: function() {
      let createdDate = new moment(this.answer.date_created)
      return createdDate.format('LLL')
    },
    modifiedTime: function() {
      let modifiedDate = new moment(this.answer.date_modified)
      return modifiedDate.format('LLL')
    },
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
