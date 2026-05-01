import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import * as authApi from '../api/auth'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const loading = ref(false)

  const isLoggedIn = computed(() => !!user.value)

  async function fetchMe() {
    try {
      const res = await authApi.getMe()
      user.value = res.data.user
    } catch {
      user.value = null
    }
  }

  async function login(email, password) {
    loading.value = true
    const res = await authApi.login({ email, password })
    user.value = res.data.user
    loading.value = false
    return res.data
  }

  async function register(data) {
    loading.value = true
    const res = await authApi.register(data)
    user.value = res.data.user
    loading.value = false
    return res.data
  }

  async function logout() {
    await authApi.logout()
    user.value = null
  }

  return { user, loading, isLoggedIn, fetchMe, login, register, logout }
})
