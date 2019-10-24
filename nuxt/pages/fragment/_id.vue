<template>
  <div>
    <h2>Fragment#{{ $route.params.id }}</h2>
    <hr/>
    <template v-if="isLoaded">
      <div>Title: {{ rawData.title }}</div>
      <div>Content: {{ rawData.content }} ({{ rawData.content.length }} Chars)</div>
      <div>Status: {{ rawData.status }}</div>
      <div>Closed At: {{ rawData.status == 'CLOSED' ? rawData.date_closed : 'Fragment is now open' }}</div>
      <div>WrittenBy: {{ rawData.avatar }}</div>
      <div>Created / Modificated At: {{ rawData.date_created }} / {{ rawData.date_modified }}</div>
      <div>Tags: {{ rawData.tags.map(v => v.name) }}</div>
      <div>
        <div>
          Votes:<br/>
          <vote :votes="rawData.votes"></vote>
        </div>
        <vote-form :target="rawData.pk"></vote-form>
      </div>
      <hr/>
      <div>
        <div v-if="rawData.comments.length > 0">
          Comments Total: {{ rawData.comments.length }} of Comments<br/>
          <comment
            v-for="comment in rawData.comments"
            :key="comment.pk"
            :target="rawData.pk"
            :comment="comment"
            @update="refresh"
            @delete="refresh"
          ></comment>
         </div>
         <div v-else>There are no comments nothing yet</div>
        <comment-form :target="rawData.pk" @created="refresh"></comment-form>
      </div>
      <hr/>
      <div>
        <div v-if="rawData.answers.length > 0">
          Answers:<br/>
          <answer
            v-for="answer in rawData.answers"
            :key="answer.pk"
            :target="rawData.pk"
            :answer="answer"
            @update="refresh"
            @delete="refresh"
          ></answer>
        </div>
        <div v-else>There is no answers nothing yet</div>
        <answer-form :target="rawData.pk" @created="refresh"></answer-form>
      </div>
      <v-btn v-if="isOwned" @click="del">Delete this fragment</v-btn>
    </template>
  </div>
</template>

<script>
import Answer from '~/components/Answer.vue'
import AnswerForm from '~/components/AnswerForm.vue'
import Comment from '~/components/Comment.vue'
import CommentForm from '~/components/CommentForm.vue'
import Vote from '~/components/Vote.vue'
import VoteForm from '~/components/VoteForm.vue'

const BASE_URL_FRAGMENT = '/api/v1/fragment'

export default {
  components: {
    'answer': Answer,
    'answer-form': AnswerForm,
    'comment': Comment,
    'comment-form': CommentForm,
    'vote': Vote,
    'vote-form': VoteForm
  },
  data: () => ({
    rawData: null,
  }),
  async asyncData ({ $axios, params }) {
    return {
      rawData: await $axios.$get(`${BASE_URL_FRAGMENT}/${params.id}`)
    }
  },
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
    async refresh () {
      this.rawData = await this.$axios.$get(`${BASE_URL_FRAGMENT}/${this.$route.params.id}`)
    },
    del () {
      this.$axios.$delete(`${BASE_URL_FRAGMENT}/${this.rawData.pk}/`)
      .then(response => {
        this.$emit('delete')
      })
      .catch(error => {
        throw Error(error)
      })
    },
  }
}
</script>
