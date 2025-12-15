import { createRouter, createWebHistory } from 'vue-router'
import RandomMovie from './components/RandomMovie.vue'
import ActorDetail from './components/ActorDetail.vue'
import MovieDetail from './components/MovieDetail.vue'

const routes = [
  {
    path: '/',
    component: RandomMovie,
    name: 'Home'
  },
  {
    path: '/actor/:id',
    component: ActorDetail,
    name: 'ActorDetail'
  },
  {
    path: '/movie/:id',
    component: MovieDetail,
    name: 'MovieDetail'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
