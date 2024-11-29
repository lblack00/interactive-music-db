import { createRouter, createWebHistory } from 'vue-router'
import Release from '../components/Release.vue'
import Master from '../components/Master.vue'
import NotFound from '../components/NotFound.vue'
import SignUp from '../components/SignUp.vue'
import Login from '../components/Login.vue'
import Home from '../components/Home.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/release/:release_id',
      name: 'Release',
      component: Release
    },
    {
      path: '/master/:master_id',
      name: 'Master',
      component: Master
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
      path: '/',
      name: 'Home',
      component: Home
    }
  ]
})

export default router
