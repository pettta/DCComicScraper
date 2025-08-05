import { createRouter, createWebHistory } from 'vue-router'
import TimelinePage from '@/pages/TimelinePage.vue'
import SubTimelinePage from '@/pages/SubTimelinePage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: TimelinePage,
      props: route => ({ selectedEras: [] }) // Default empty selections
    },
    {
      path: '/timeline',
      name: 'timeline',
      component: SubTimelinePage,
      props: route => ({ 
        selectedEras: route.query.sections ? 
          (Array.isArray(route.query.sections) ? route.query.sections : [route.query.sections]) : 
          []
      })
    }
  ]
})

export default router
