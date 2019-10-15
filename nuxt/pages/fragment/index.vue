<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12" md="9" order="2" order-md="1">
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
    <v-row>
      <v-btn @click="load">Load more</v-btn>
    </v-row>
  </v-container>
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