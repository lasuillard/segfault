<template>
<div>
    <div class="ac-banner white-text col-12">
        <div class="row sub-banner">
            <div class="container" style="max-width: 70%;">
                <div class="col-sm12 col-md6 acinfo">
                    <hh class="userinfo"><b>Activity</b></hh>
                    <p class="userinfo subinfo" style="font-size: 16px;">Post new fragment</p>
                </div>
                <div class="col-sm12 col-md6 sbinfo">
                </div>
            </div>
        </div>
    </div>
    <div class="container " style="max-width: 70%; min-height: 105vh !important;">
      <!--h1>Activity</h1>
      Profile: {{ profile }}
      <hr-->

      <!--notification-window></notification-window-->
      <fragment-form @created="load"></fragment-form>
      <br/>
      <!-- <hr/>

      My Recent Fragments: {{ recentFragments }}

      <hr/>

      Related Fragments (Tagged with my latest fragment's tags for now):
      {{ relatedFragments }} -->

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
import NotificationWindow from '~/components/NotificationWindow.vue'
import FragmentForm from '~/components/FragmentForm.vue'
import { mapGetters } from 'vuex'

export default {
  components: {
    'notification-window': NotificationWindow,
    'fragment-form': FragmentForm,

  },
  data: () => ({
    recentFragments: null,
    relatedFragments: null,
    reactionsOnMyContents: null
  }),
  computed: {
    ...mapGetters({
      profile: 'user/getProfile',
      isLoggedIn: 'user/isLoggedIn'
    })
  },
  methods: {
    async load () {
      this.recentFragments = await this.$axios.$get(`/api/v1/fragment?avatar=${ this.profile.avatar.pk }`)
      var recentTags = []
      for (var f of this.recentFragments.results) {
        recentTags = recentTags.concat(f.tags)
      }
      recentTags = Array.from(new Set(recentTags.map(t => t.name)))
      this.relatedFragments = await this.$axios.$get(`/api/v1/fragment?tags=${ recentTags.join(',') }`)
    }
  },
  async created () {
    if (!this.isLoggedIn)
      return

    await this.load()
  },
  beforeRouteEnter (to, from, next) {
    next(vm => {
      if (!vm.$store.getters['user/isLoggedIn']) {
        alert('You need to login')
        vm.$router.replace({ name: 'index' })
        next(false)
      }
      else
        next(true)
    })
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
