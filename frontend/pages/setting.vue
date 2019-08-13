<template>
  <v-card>
    <v-list subheader>
      <v-subheader>Visual configurations</v-subheader>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>Theme</v-list-item-title>
          <v-radio-group 
            class="px-2"
            v-model="localChanges.theme"
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
      
      <v-divider />
      
    </v-list>
    <v-card-actions>
      <v-spacer />
      <v-btn color="secondary" @click="resetConfig">Reset</v-btn>
      <v-btn color="primary" @click="saveConfig({ ...localChanges })">Save</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import { mapGetters, mapMutations, mapActions } from 'vuex'
import { SET_DATA_FIELD } from '~/store/mutation-types'

const DEFAULT_SETTING = {
  theme: 'light'
}

export default {
  data: () => ({
    localChanges: {
      ...DEFAULT_SETTING
    }
  }),
  computed: {
    ...mapGetters({
      isLoggedIn: 'user/isLoggedIn',
      config: 'user/getConfig'
    }),
    themesSupported () {
      return Object.keys(this.$vuetify.theme.themes).map(str => ({
        display: str[0].toUpperCase() + str.slice(1),
        value: str
      }))
    }
  },
  methods: {
    ...mapActions({
      saveConfig: 'user/saveConfig'
    }),
    resetConfig () {
      for (var key in DEFAULT_SETTING)
        this.localChanges[key] = DEFAULT_SETTING[key]
    }
  }
}
</script>
