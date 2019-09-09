<template>
  <v-app>
    <!-- Top navigation bar -->
    <v-app-bar app v-bind="getThemeObj">
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
          <login-dialog />
        </v-dialog>
        <v-btn :to="{ name: 'sign' }" text outlined>Sign up</v-btn>
      </template>
    </v-app-bar>

    <!-- Side navigation menu -->
    <v-navigation-drawer
      app
      v-model="isDrawerOpen"
      v-bind="getThemeObj"
    >
      <v-list>
        <v-list-item>
          <v-list-item-avatar>
            <v-img :src="profile.profile_image" />
          </v-list-item-avatar>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title class="title">
              {{ profile.display_name }}
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

    <!-- Content -->
    <v-content v-bind="getThemeObj">
      <v-container fluid>
        <nuxt />
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import { mapState, mapGetters, mapMutations, mapActions } from 'vuex'
import LoginDialogVue from '../components/LoginDialog.vue';

export default {
  components: {
    'login-dialog': LoginDialogVue
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
          icon: 'mdi-account',
          link: { name: 'activity' }
        },
        { 
          title: 'Fragment',
          icon: 'mdi-view-dashboard-variant',
          link: { name: 'fragment'}
        },
        {
          title: 'Setting',
          icon: 'mdi-settings',
          link: { name: 'setting' }
        }
      ]
    }
  }),
  computed: {
    ...mapGetters({
      isLoggedIn: 'user/isLoggedIn',
      profile: 'user/getUserProfile',
      config: 'user/getConfig'
    }),
    getThemeObj () {
      // convert theme configuration into vuetify theme object
      return {
        [this.config.theme]: true
      }
    }
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
