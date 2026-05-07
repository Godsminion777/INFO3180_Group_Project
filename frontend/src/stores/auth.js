import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import * as authApi from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const authChecked = ref(false)
  const loading = ref(false)

  const isLoggedIn = computed(() => !!user.value)

  async function login(email, password) {
    loading.value = true
    try {
      const res = await authApi.login({ email, password })
      user.value = res.data.user
      return res.data
    } finally {
      loading.value = false
    }
  }

  async function register(data) {
    loading.value = true
    try {
      const res = await authApi.register(data)
      user.value = res.data.user
      return res.data
    } finally {
      loading.value = false
    }
  }

  async function fetchMe() {
    console.log('fetchMe called from:', new Error().stack)
    try {
      const res = await authApi.me()
      user.value = res.data.user
    } catch {
      user.value = null
    } finally {
      authChecked.value = true
    }
  }

  async function logout() {
    await authApi.logout()
    user.value = null
  }

  return { user, loading, isLoggedIn, login, register, fetchMe, logout, authChecked }
})
