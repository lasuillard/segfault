<template v-if="isLoaded">
  <div style="background: #FFFFFF">
    <div class="ac-banner white-text col-12">
        <div class="row sub-banner">
            <div class="container" style="max-width: 80%;">
                <div class="col-sm12 col-md6 acinfo">
                    <hh class="userinfo"><b>Fragment #{{ $route.params.id }}</b></hh>
                    <p class="userinfo subinfo" style="font-size: 16px;"></p>
                </div>
                <div class="col-sm12 col-md6 sbinfo">
                </div>
            </div>
        </div>
    </div>
    <div class="container" style="max-width: 80%; ">
      <div class="row">
        <div class="col-8" style="margin-top: 30px;">
          <div style="min-height: 40px; display: inline-block; width: 100%; margin-bottom: 20px">
            <div style="width: 40px; float: left;">
              <img :src="rawData.avatar.profile_image" style="display: inline; height: 40px; width: 42.1053px; margin-left: 0px;"/>
            </div>
            <div style="padding-left: 52px;">
              <div style="padding-top: 12.5px;">
                <a style="font-family: Segoe UI Semibold,Segoe UI,SegoeUI; font-size: 16px; color: #0067b8;">{{ rawData.avatar.display_name }}</a>
                <span style="float: right;">
                  <p style="display: inline; color: #5e5e5e; font-family: Segoe UI,SegoeUI,Helvetica,Arial,sans-serif; font-size: 16px;">Created on {{ rawData.date_created }}</p>
                </span>
              </div>
            </div>
          </div>
          <h1 style="font-weight: 600; font-size: 34px; line-height: 40px; font-family: Segoe UI,SegoeUI,Helvetica,Arial,sans-serif; margin: 0px;">{{ rawData.title }}</h1>
          <div style="margin-top: 18px; display: block; word-wrap: break-word; font-family: Segoe UI,SegoeUI,Helvetica,Arial,sans-serif;">
            {{ rawData.content }}
          </div>
          <v-row
            align="center"
            justify="end"
          >
            <a v-if="isOwned" @click="del" style="margin-top: 20px; color: #900020">Delete this fragment</a>
          </v-row>
          <div style="margin-top: 24px; margin-bottom: 32px;">
            <h2 style="padding-top: 24px; padding-bottom: 24px; font-weight: 600; font-size: 20px; line-height: 24px; font-family: Segoe UI,SegoeUI,Helvetica,Arial,sans-serif; ">
              Comments({{ rawData.comments.length }})
            </h2>
            <div v-if="rawData.comments.length > 0">
              <comment
                v-for="comment in rawData.comments"
                :key="comment.pk"
                :target="rawData.pk"
                :comment="comment"
                @update="refresh"
                @delete="refresh"
              ></comment>
            </div>
            <comment-form :target="rawData.pk" @created="refresh"></comment-form>
          </div>
        </div>
        <div class="col-1"></div>
        <div class="col-3">
          <h2 style="font-size: 20px; line-height: 24px; margin-top: 30px;">Article Info</h2>
          <hr class="separator-line" style="margin-top: 12px;">
          <span class="infoTop">
            Modificated At {{ rawData.date_modified }}
          </span>
          <span class="infoMiddle">
            Status: {{ rawData.status == 'CLOSED' ? rawData.date_closed : 'OPEN' }}
          </span>
          <span class="infoMiddle">
            Tags: 
            {{ rawData.tags.map(v => v.name) }}
          </span>
        </div>
      </div>
    </div>
    <div style="background-color: #f2f2f2; padding-top: 1px; display: inline-block; width: 100%; vertical-align: bottom;">
      <div class="container" style="max-width: 80%;">
        <div class="row">
          <div class="col-8">
            <h2 style="padding-top: 24px; padding-bottom: 24px; font-weight: 600; font-size: 20px; line-height: 24px; font-family: Segoe UI,SegoeUI,Helvetica,Arial,sans-serif; ">
                Answers({{ rawData.answers.length }})
            </h2>
            <div v-if="rawData.answers.length > 0">
              <answer
                v-for="answer in rawData.answers"
                :key="answer.pk"
                :target="rawData.pk"
                :answer="answer"
                @update="refresh"
                @delete="refresh"
              ></answer>
            </div>
            <answer-form :target="rawData.pk" @created="refresh"></answer-form>
          </div>
          <div class="col-1"></div>
          <div class="col-3"></div>
        </div>
      </div>
    </div>
      <footer id="footer" class="page-footer dk">
          <div class="footer-copyright dk">
              <div class="container" style="max-width: 70%; color: rgba(255,255,255,0.8);">
              © 2019 SegFault, All rights reserved. 
              <a class="grey-text text-lighten-4 right" href="#!"></a>
              </div>
          </div>
      </footer>
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
     tagArray: [],
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
    },
    makingTagArray: function() {
      let test = this.rawData.tags.map(v => v.name)
      let i;
      for(i=0; i<test.length; i++) {
      this.tagArray.push(test[i])
      }
    },
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
<style>
.separator-line {
    border: 1px solid;
    border-top: none;
    border-right: none;
    border-left: none;
    height: 1px;
    color: #d2d2d2;
    border-color: #d2d2d2;
    background-color: #fff;
    margin: 0 0 0 0;
    clear: both;
}
.infoTop {
  display: block; 
  font-size: 15px; 
  margin-top: 16px;
}
.infoMiddle {
  display: block;
  margin-top: 20px;
  margin-bottom: 20px;
  font-size: 15px;
}
</style>
