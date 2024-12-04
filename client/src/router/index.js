import { createRouter, createWebHistory } from 'vue-router'
import Release from '../components/Release.vue'
import Master from '../components/Master.vue'
import NotFound from '../components/NotFound.vue'
import SignUp from '../components/SignUp.vue'
import Login from '../components/Login.vue'
import Home from '../components/Home.vue'
import ArtistPage from '../components/ArtistPage.vue'
import SongPage from '@/components/SongPage.vue'
import SearchResults from '../components/SearchResults.vue'

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
      path: '/',
      name: 'Home',
      component: Home
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
      path: '/artist/:artist_id',
      name: 'ArtistPage',
      component: ArtistPage
    },
    {
      path: '/song/songPage',
      name: 'SongPage',
      component: SongPage
    },
    {
      path: '/search/:query',
      name: 'SearchResults',
      component: SearchResults,
      props: route => ({
        query: route.params.query,
        filterOption: route.query.filterOption,
        genreOption: route.query.genreOption
      }),
    },
  ]
})

export default router
