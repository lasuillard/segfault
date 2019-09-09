import Vue from 'vue'
import VeeValidate from 'vee-validate'

const config = {
  inject: true,
  fieldsBagName: 'veeFields', 
  errorBagName: 'veeErrors'
}

Vue.use(VeeValidate, config)
