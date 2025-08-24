import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LandingPage from '../views/LandingPage.vue'
import ViewCampaigns from '@/views/ViewCampaigns.vue'
import EditCampaigns from '@/views/EditCampaigns.vue'
import Leaderboard from '@/views/Leaderboard.vue'
import PaymentPage from '@/views/PaymentPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/home',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/',
      name: 'landing',
      component: LandingPage
    },
    {
      path: '/viewcampaigns',
      name: 'viewcampaigns',
      component: ViewCampaigns
    },
    {
      path: '/editcampaigns',
      name: 'editacampaigns',
      component: EditCampaigns
    },
    {
      path: '/leaderboard',
      name: 'leaderboard',
      component: Leaderboard
    },
    {
      path: '/payment',
      name: 'payment',
      component: PaymentPage
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
  ],
})

export default router
