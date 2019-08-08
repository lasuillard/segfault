<template>
  <v-card>
    <v-list subheader>
      <v-subheader>Visual configurations</v-subheader>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>Theme</v-list-item-title>
          <v-radio-group 
            class="px-2"
            v-model="themeSelected"
            row
          >
            <v-radio
              v-for="theme in themesSupported"
              :key="theme.value"
              :label="theme.display"
              :value="theme.value"
            />
          </v-radio-group>
        </v-list-item-content>
      </v-list-item>
    </v-list>
    <v-card-actions>
      <v-spacer />
      <v-btn color="secondary" @click="resetConfig">Reset</v-btn>
      <v-btn color="primary" @click="saveConfig">Save</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import { mapState, mapMutations, mapActions } from 'vuex'
import { CHANGE_CONFIG } from '~/store/mutation-types'

export default {
  computed: {
    ...mapState({
      '_theme': 'theme'
    }),
    themesSupported () {
      return Object.keys(this.$vuetify.theme.themes).map(str => ({
          display: str[0].toUpperCase() + str.slice(1),
          value: str
        })
      )
    },
    themeSelected: {
      get: function () {
        return this._theme
      },
      set: function (newTheme) {
        this.changeConfig({ key: 'theme', value: newTheme })
      }
    }
  },
  methods: {
    ...mapMutations({
      'changeConfig': CHANGE_CONFIG
    }),
    ...mapActions({
      'saveConfig': 'saveConfig',
      'resetConfig': 'resetConfig'
    })
  }
}
</script>
