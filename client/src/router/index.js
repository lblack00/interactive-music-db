import { createRouter, createWebHistory } from 'vue-router'
import Release from '../components/Release.vue'
import NotFound from '../components/NotFound.vue'
import SignUp from '../components/SignUp.vue'
import Login from '../components/Login.vue'
import Ping from '../components/Ping.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/release/:release_id',
      name: 'Release',
      component: Release
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: NotFound
    },
    {
      path: '/signup',
      name: 'SignUp',
      component: SignUp
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping
    }
  ]
})

export default router
