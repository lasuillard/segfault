<template>
<!--  <v-app :style="{ background: $vuetify.theme.themes.dark.warning }"> -->
  <v-app>
    <!-- Top navigation bar -->
    <v-app-bar app v-bind="theme">
      <v-app-bar-nav-icon @click="isDrawerOpen = !isDrawerOpen" />
      <v-toolbar-title>SegFault</v-toolbar-title>

      <v-spacer />

      <!-- Guest -->
      <template v-if="isLoggedIn">
        <v-btn @click="logout" text outlined>Logout</v-btn>
      </template>

      <!-- Authenticated user -->
      <template v-else>
        <v-dialog v-model="isSignInOpen" max-width="400px">
          <template v-slot:activator="{ on }">
            <v-btn text outlined class="mr-3" v-on="on">Sign in</v-btn>
          </template>

          <!-- Login modal component -->
          <login-dialog></login-dialog>

        </v-dialog>
        <v-btn :to="{ name: 'sign' }" text outlined>Sign up</v-btn>
      </template>
    </v-app-bar>

    <!-- Side navigation menu -->
    <v-navigation-drawer
      app
      v-model="isDrawerOpen"
      v-bind="theme"
    >
      <v-list>
        <v-list-item>
          <v-list-item-avatar>
            <v-img :src="profile.avatar.profile_image" />
          </v-list-item-avatar>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title class="title">
              {{ profile.avatar.display_name }}
            </v-list-item-title>
            <v-list-item-subtitle>
              {{ profile.email }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>

      <v-divider />

      <v-list>
        <v-list-item
          v-for="item in items.drawer" 
          :key="item.title"
          :to="item.link"
          exact
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <notification-box />

    <!-- Content -->
    <v-content v-bind="theme">
        <nuxt />
    </v-content>
    
  </v-app>
</template>

<script>
import { mapState, mapGetters, mapMutations, mapActions } from 'vuex'
import LoginDialogVue from '../components/LoginDialog'
import NotificationBox from '../components/NotificationBox'

export default {
  components: {
    'login-dialog': LoginDialogVue,
    'notification-box': NotificationBox
  },
  data: () => ({
    isDrawerOpen: false,
    isSignInOpen: false,
    items: {
      drawer: [
        { 
          title: 'Home',
          icon: 'mdi-home',
          link: { name: 'index' } 
        },
        {
          title: 'Activity',
          icon: 'post_add',
          link: { name: 'activity' }
        },
        { 
          title: 'Fragment',
          icon: 'mdi-view-dashboard-variant',
          link: { name: 'fragment' }
        },
        {
          title: 'Live Chat (in preview)',
          icon: 'mdi-forum',
          link: { name: 'chat' }
        },
        {
          title: 'Settings',
          icon: 'mdi-settings',
          link: { name: 'setting' }
        }
      ],
    }
  }),
  computed: {
    ...mapGetters({
      isLoggedIn: 'user/isLoggedIn',
      profile: 'user/getProfile',
      theme: 'user/getThemeObj'
    }),
  },
  methods: {
    ...mapActions({
      logout: 'user/logout'
    })
  },
  watch: {
    '$route': function (route, oldRoute) {
      // when changing route, close dialog
      this.isSignInOpen = false
    }
  }
}
</script>
