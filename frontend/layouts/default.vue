<template>
  <v-app>
    <v-app-bar
      app
      hide-on-scroll
      v-bind="theme"
    >
      <v-app-bar-nav-icon
        @click="openNavBar = !openNavBar"
      />
      <v-toolbar-title>SegFault</v-toolbar-title>
      <v-layout
        justify-end
      >
        <v-btn icon
          color="success"
          large
          :disabled="!isLoggedIn"
          :to="{ name: 'user' }"
        >
          <v-icon>mdi-account</v-icon>
        </v-btn>
      </v-layout>
    </v-app-bar>

    <v-navigation-drawer
      app
      v-bind="theme"
      v-model="openNavBar">
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title class="title">
            Application
          </v-list-item-title>
          <v-list-item-subtitle>
            subtext
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>

      <v-divider />

      <v-list>
        <v-list-item
          v-for="item in items" 
          :key="item.title"
          :to="item.link"
          exact>
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-content
      v-bind="theme"
    >
      <v-container fluid>
        <nuxt/>
      </v-container>
    </v-content>

    <v-footer
      app
      fixed
      v-bind="theme"
    >
      SegFault
    </v-footer>
  </v-app>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  data () {
    return {
      openNavBar: false,
      items: [
        { 
          title: 'Home',
          icon: 'mdi-home',
          link: { name: 'index' } 
        },
        { 
          title: 'Fragment',
          icon: 'mdi-view-dashboard-variant',
          link: { name: 'fragment'}
        },
        { 
          title: 'About',
          icon: 'mdi-help-box',
          link: { name: 'about' }
        },
      ],
    }
  },
  computed: {
    ...mapGetters({
      isLoggedIn: 'user/isLoggedIn',
      theme: 'getCurrentTheme'
    })
  }
}
</script>
