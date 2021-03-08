import Vue from 'vue'
import App from './App.vue'
import router from './router'

import VueApexCharts from 'vue-apexcharts'
import AsyncComputed from 'vue-async-computed'

Vue.use(AsyncComputed)

Vue.config.productionTip = false


// Globally register your component
Vue.component('apexchart', VueApexCharts);


new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
