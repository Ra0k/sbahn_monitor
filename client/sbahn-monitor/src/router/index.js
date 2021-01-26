import Vue from 'vue'
import VueRouter from 'vue-router'
import General from '../views/General.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/general',
    name: 'General',
    component: General
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/heatmap',
    name: 'HeatmapChart',
    component: () => import(/* webpackChunkName: "about" */ '../views/HeatmapChart.vue')

  },

  {
    path: '/planYourTrip',
    name: 'planYourTrip',
    component: () => import(/* webpackChunkName: "about" */ '../views/PlanYourTrip.vue')

  },

]

const router = new VueRouter({
  routes
})

export default router
