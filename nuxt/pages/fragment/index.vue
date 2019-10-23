<template>
<div>
  <div class="ac-banner white-text col-12">
      <div class="row sub-banner">
          <div class="container" style="max-width: 70%;">
              <div class="col-sm12 col-md6 acinfo">
                  <hh class="userinfo"><b>Fragment</b></hh>
                  <p class="userinfo subinfo" style="font-size: 16px;">See all fragments</p>
              </div>
              <div class="col-sm12 col-md6 sbinfo">
              </div>
          </div>
      </div>
  </div>
  <div class="container" style="max-width: 70%; min-height: 105vh !important;">
    <v-row>
      <v-col cols="12">
        <v-sheet 
          v-for="item in items"
          :key="item.pk"
          class="pa-3 px-4 my-4"
          elevation="1"
          @click="$router.push({ name: 'fragment-id', params: { id: item.pk } })"
        >
          <v-row>
            <v-col cols="3" md="2" align-self="center">
              <div class="mb-2 body-1 text-center">
                {{ item.pk }}
              </div>
              <v-divider />
              <div class="mt-2 text-center">
                <v-icon>
                  {{ item.is_closed ? 'mdi-lock-outline' : 'mdi-lock-open-variant-outline' }}
                </v-icon>
              </div>
            </v-col>
            <v-col cols="9" md="10">
              <v-row class="mb-2" no-gutters>
                <v-col>
                  <div class="title" style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{{ item.title }}</div>
                  <div class="subtitle-2">by {{ item.avatar.display_name }}, {{ getTimeDeltaStr(item.date_created) }}</div>
                </v-col>
              </v-row>
              <v-row no-gutters>
                <v-col align-self="start">
                  <div class="caption">{{ item.count_answer }} Answers, {{ item.count_vote }} Votes, {{ item.count_comment }} Comments</div>
                </v-col>
              </v-row>
            </v-col>
          </v-row>
        </v-sheet>
      </v-col>
      <v-col cols="12" md="3" order="1" order-md="2">

      </v-col>
    </v-row>
    <v-row style="margin-bottom: 40px;">
      <v-btn @click="load">Load more</v-btn>
    </v-row>

    <v-btn
       class="mx-2"
       color="primary"
       dark
       absolute
       bottom
       right
       fab
       large
       style="bottom: 0; position: absolute; margin: 0 0 16px 16px;"
      >
       <v-icon>mdi-pencil</v-icon>
   </v-btn>

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

export default {
  data: () => ({
    rawData: null,
    items: [],
  }),
  computed: {
    isEnd: function () {
      return this.rawData && this.rawData.next == null
    }
  },
  methods: {
    async load () {
      if (this.rawData && this.rawData.hasOwnProperty('next')) {
        this.rawData = await this.$axios.$get(this.rawData.next)
      } 
      else {
        this.rawData = await this.$axios.$get('/api/v1/fragment')
      }
      let fragments = this.rawData.results
      this.items = this.items.concat(fragments)
    },
    getTimeDeltaStr(date) {
      var milliseconds = Date.now() - new Date(date)
      var seconds = Math.round(milliseconds / 1000)
      var minutes = Math.round(seconds / 60)
      if (minutes == 0)
        return `${seconds} seconds ago`
      
      var hours = Math.round(minutes / 60)
      if (hours == 0)
        return `${minutes} minutes ago`

      var days = Math.round(hours / 24)
      if (days == 0)
        return `${hours} hours ago`

      return `${days} days ago`
    }
  },
  created () {
    this.load()
  }
}
</script>
<style>
/* 상단 배너관련 css */
.ac-banner {
    background: linear-gradient(to bottom,#005799 0,#0076d1);
    box-shadow: 0 12px 45px -8px rgba(0,120,215,.35);
}
.sub-banner {
    padding-top: 20px;
    padding-bottom: 20px;
}
.acinfo {
    margin-top: 14px;
}
.sbinfo{
    margin-top: 14px;
}
.userinfo {
    margin-top: 0px;
    margin-bottom: 0px;
}
.midinfo {
    font-size: 15px;
}
.subinfo {
    color: #96cbed;
    margin-top: 5px;
    font-size: 13px;
}
hh {
    font-size: 2.28rem;
    line-height: 110%;
    margin: 1.52rem 0 .912rem 0;
}
</style>