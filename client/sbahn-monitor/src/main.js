import Vue from 'vue'
import App from './App.vue'
import router from './router'

import VueApexCharts from 'vue-apexcharts'
import vuetify from '@/plugins/vuetify' // path to vuetify export

Vue.config.productionTip = false


// Globally register your component
Vue.component('apexchart', VueApexCharts);


new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')
