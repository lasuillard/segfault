<template>
  <div>
    <template v-if="isLoaded">
      <v-card
        class="mx-auto"
        color="#F2F2F2"
        style="margin-bottom: 20px;"
      >
        <v-card-title>
            <v-list-item-avatar>
              <v-img
                class="elevation-6"
                :src="comment.avatar.profile_image"
              ></v-img>
            </v-list-item-avatar>
    
            <v-list-item-content>
              <v-list-item-title>
                <a style="font-family: Segoe UI Semibold,Segoe UI,SegoeUI; font-size: 16px; color: #0067b8;">{{comment.avatar.display_name}}</a>
                <span style="float: right;">
                  <p style="display: inline; color: #5e5e5e; font-family: Segoe UI,SegoeUI,Helvetica,Arial,sans-serif; font-size: 16px;">Created on {{ createdTime }}</p>
                </span>  
              </v-list-item-title>
            </v-list-item-content>
        </v-card-title>
    
        <v-card-text style="font-size: 15px; font-family: Segoe UI,SegoeUI,Helvetica Neue,Helvetica,Arial,sans-serif; color: #000;">
          {{comment.content}}
        </v-card-text>
    
        <v-card-actions>
          <v-list-item class="grow">
            <v-row
              align="center"
              justify="end"
            >
              <a v-if="isOwned" @click="del">
                <v-icon>delete_forever</v-icon>
              </a>
            </v-row>
          </v-list-item>
        </v-card-actions>
      </v-card>
    </template>
  </div>
</template>

<script>
import moment from 'moment'

const BASE_URL_COMMENT = '/api/v1/comment'

export default {
  props: {
    target: { // parent commentable object id this comment related with
      type: Number,
      required: true
    },
    comment: { // primary key and extra informations
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
      return this.rawData && this.rawData.hasOwnProperty('pk')
    },
    isOwned: function () {
      let profile = this.$store.getters['user/getProfile']
      return profile.avatar.hasOwnProperty('pk') && profile.avatar.pk == this.rawData.avatar.pk
    },
    createdTime: function() {
      let createdDate = new moment(this.comment.date_created)
      return createdDate.format('LLL')
    },
    modifiedTime: function() {
      let modifiedDate = new moment(this.comment.date_modified)
      return modifiedDate.format('LLL')
    },
  },
  methods: {
    async load () {
      this.rawData = await this.$axios.$get(`${BASE_URL_COMMENT}/${this.comment.pk}`)
    },
    patch () {
      this.$axios.$patch(`${BASE_URL_COMMENT}/${this.comment.pk}/`, { 
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
      this.$axios.$delete(`${BASE_URL_COMMENT}/${this.comment.pk}/`)
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
