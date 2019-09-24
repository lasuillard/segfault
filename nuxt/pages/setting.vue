<template>
  <v-card>
    <v-list subheader>
      <v-subheader>Visual Configurations</v-subheader>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>Theme</v-list-item-title>
          <v-radio-group 
            class="px-2"
            v-model="localChanges.theme"
            row
          >
            <v-radio
              v-for="theme in supportedThemes"
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
      <v-btn color="primary" :disabled="isChangeOccurred" @click="saveConfig({ ...localChanges })">Save</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import { DEFAULT_CONFIG } from '~/store/user'


export default {
  data: () => ({
    oldSetting: null,
    localChanges: null,
    isChangeOccurred: false,
  }),
  computed: {
    ...mapGetters({
      isLoggedIn: 'user/isLoggedIn',
      config: 'user/getConfig'
    }),
    supportedThemes () {
      return Object.keys(this.$vuetify.theme.themes).map(str => ({
        display: str[0].toUpperCase() + str.slice(1),
        value: str
      }))
    },
  },
  methods: {
    ...mapActions({
      saveConfig: 'user/saveConfig'
    }),
    resetConfig () {
      for (var key in DEFAULT_SETTING)
        this.localChanges[key] = DEFAULT_SETTING[key]
    }
  },
  watch: {
    localChanges: {
      handler: function (val, oldVal) {
        console.log('Change: ', oldVal, val)
        console.log(this.oldSetting)
        for (var key in this.oldSetting) { 
          console.log(key)
          if (this.oldSetting[key] != val[key]) {
            this.isChangeOccurred = true
            return
          }
        }
        this.isChangeOccurred = false
      },
      deep: true,
    }
  },
  created () {
    this.oldSetting = { ...this.config }
    this.localChanges = { ...this.config }
  },
}
</script>
