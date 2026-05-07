import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  { path: '/', redirect: '/browse' },
  { path: '/login', component: () => import('@/views/LoginView.vue'), meta: { guest: true } },
  { path: '/register', component: () => import('@/views/RegisterView.vue'), meta: { guest: true } },
  { path: '/browse', component: () => import('@/views/BrowseView.vue'), meta: { auth: true } },
  { path: '/profile/:id', component: () => import('@/views/ProfileView.vue'), meta: { auth: true } },
  { path: '/profile/:id/edit', component: () => import('@/views/EditProfileView.vue'), meta: { auth: true } },
  { path: '/matches', component: () => import('@/views/MatchesView.vue'), meta: { auth: true } },
  { path: '/messages', component: () => import('@/views/MessagesView.vue'), meta: { auth: true } },
  { path: '/messages/:userId', component: () => import('@/views/ChatView.vue'), meta: { auth: true } },
  { path: '/search', component: () => import('@/views/SearchView.vue'), meta: { auth: true } },
  { path: '/saved', component: () => import('@/views/SavedView.vue'), meta: { auth: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to) => {
  const auth = useAuthStore()
  if (!auth.authChecked) await auth.fetchMe()

  if (to.meta.auth && !auth.isLoggedIn) return '/login'
  if (to.meta.guest && auth.isLoggedIn) return '/browse'
})

export default router
