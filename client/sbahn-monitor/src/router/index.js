import Vue from 'vue'
import VueRouter from 'vue-router'
import Statistics from '../views/Statistics.vue'
import AlertsInterface from '../views/AlertsInterface.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/stats',
    name: 'Statistics',
    component: Statistics
  },
  // {
  //   path: '/about',
  //   name: 'About',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  // },
  // {
  //   path: '/heatmap',
  //   name: 'HeatmapChart',
  //   component: () => import(/* webpackChunkName: "about" */ '../views/HeatmapChart.vue')

  // },

  // {
  //   path: '/Stats_Routing',
  //   name: 'RoutingStats',
  //   component: () => import(/* webpackChunkName: "about" */ '../views/Stats_Routing.vue')

  // },
  {
    path: '/',
    name: 'Routing',
    component: () => import(/* webpackChunkName: "about" */ '../views/Routing.vue')

  },
  {
    path: '/alerts',
    name: 'Alerts',
    component: AlertsInterface
  }

]

const router = new VueRouter({
  routes
})

export default router
