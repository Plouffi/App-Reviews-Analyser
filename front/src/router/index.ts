import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'
import Scraper from '../components/Scraper.vue'
import Analyser from '../components/Analyser.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/home',
      name: 'home',
      component: Home
    },
    {
      path: '/scraper',
      name: 'scraper',
      component: Scraper
    },
    {
      path: '/analyser',
      name: 'analyser',
      component: Analyser
    }
  ]
})

router.beforeEach((to, from) => {
  const toDepth = to.path.split('/').length
  const fromDepth = from.path.split('/').length
  to.meta.transition = 'fade'
})

export default router
