<!--template>
    <v-container>
      <h2>Editor</h2>
      <div style="margin-top: 50px; margin-bottom: 50px;">
      <editor v-model="editorText" />
      </div>
      <h2>Preview</h2>
      <div style="margin-top: 50px; outline: 2px solid grey; padding: 10px">
        <viewer :value="editorText" />
      </div>

  </v-container>
</template>
<script>

import { Editor, Viewer } from '@toast-ui/vue-editor'
import 'tui-editor/dist/tui-editor.css';
import 'tui-editor/dist/tui-editor-contents.css';
import 'codemirror/lib/codemirror.css';

export default {

    components: {
      'editor': Editor,
      'viewer': Viewer
    },
    data() {
        return {
          editorText: "Enter Here",
        };
    },
};
</script-->
<template>
<<<<<<< HEAD
  <v-card light flex-column>
<!-- 뷰어 부분 -->
<v-card-title text>Making Fragment</v-card-title>
    <v-card-text>
      <p>Fragment 미리보기</p>
      <v-divider></v-divider>
      <viewer :value="editorText" />
      <v-divider></v-divider>
    </v-card-text>
  <editor v-model="editorText"/>
  <div style="margin-top: 20px;">

    <!--분류 설정 넣기-->

    <v-btn text color="primary">Done</v-btn>
  </div>
</v-card>

</template>

<script>

import { Editor, Viewer } from '@toast-ui/vue-editor'
import 'tui-editor/dist/tui-editor.css';
import 'tui-editor/dist/tui-editor-contents.css';
import 'codemirror/lib/codemirror.css';

export default {

    components: {
      'editor': Editor,
      'viewer': Viewer
    },
    data() {
        return {
          editorText: "",
        };
    },
};
</script>

<style>

</style>


<!-- 에디터 부분 -->
    <!-- <v-textarea
      label="내용"
      persistent-hint
      required
      v-model="form.content"
    ></v-textarea> -->
=======
  <div>
    <h2>Activity</h2>
    Profile: {{ profile }}
    <hr/>
    <notification-window></notification-window>
    <hr/>
    Post new fragment: <fragment-form @created="load"></fragment-form>
    <hr/>
    My Recent Fragments: {{ recentFragments }}
    <hr/>
    Related Fragments (Tagged with my latest fragment's tags for now):
    {{ relatedFragments }}
  </div>  
</template>

<script>
import NotificationWindow from '~/components/NotificationWindow.vue'
import FragmentForm from '~/components/FragmentForm.vue'
import { mapGetters } from 'vuex'

export default {
  components: {
    'notification-window': NotificationWindow,
    'fragment-form': FragmentForm
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
>>>>>>> 1d76bf84b4186142ed108d44756f4a4d08bca995
