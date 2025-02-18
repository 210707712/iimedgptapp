import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'
import iimedgpt from '@/views/iimedgpt.vue'
import daozhen from '@/views/daozhen.vue'
import SoltShow from '@/views/SoltShow.vue'
import zl from '@/views/zl.vue'
Vue.use(VueRouter)

const routes = [
  // {
  //   path: '/',
  //   name: 'home',
  //   component: HomeView
  // },
  // {
  //   path: '/',
  //   name: 'iimedgpt',
  //   component: iimedgpt
  // },
  {
    path: '/',
    name: 'zl',
    component: zl
  },
  {
    path: '/daozhen',
    name: 'daozhen',
    component: daozhen
  },
  {
    path: '/soltshow',
    name: 'SoltShow',
    component: SoltShow
  },
]

const router = new VueRouter({
  routes
})

export default router
