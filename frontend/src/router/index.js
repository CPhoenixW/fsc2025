import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '../views/LandingPage.vue'
import LoginPage from '../views/LoginPage.vue'
import RegisterPage from '../views/RegisterPage.vue'
import ContentPage from '../views/ContentPage.vue'


const routes = [
  { path: '/', component: LandingPage },
  { path: '/login', component: LoginPage },
  {path: '/manager',component: ContentPage,
    children: [
      {path: 'indexPage',component: () => import('../views/manager/IndexPage.vue')},
      {path: 'personPage',component: () => import('../views/manager/PersonPage.vue')},
      {path: 'generate',component: () => import('../views/manager/GenerateSpeechPage.vue')},
      {path: 'clone',component: () => import('../views/manager/CloneVoicePage.vue')},
      {path: 'managePage',component: () => import('../views/manager/ManagePage.vue')},
      {path: 'audio',component: () => import('../views/manager/AudioPage.vue')},
      {path: 'digit',component: () => import('../views/manager/DigitPage.vue')},
    ],
    meta: { requiresAuth: true }
  },
  { path: '/register', component: RegisterPage },
  { path: '/content', component: ContentPage },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router