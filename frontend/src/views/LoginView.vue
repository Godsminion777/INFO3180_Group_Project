<template>
  <div class="min-h-screen flex items-center justify-center bg-linear-to-br from-blue-100 to-pink-100 dark:from-blue-950 dark:to-pink-950 px-4">
    <div class="w-full max-w-md bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6">
      <div class="text-center mb-8">
        <div class="text-5xl mb-3">🌊</div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100">DriftDater</h1>
        <p class="text-gray-500 dark:text-gray-400 text-sm mt-1">🩵Go with the flow🩵</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Email</label>
          <input
            v-model="form.email"
            type="email"
            required
            class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-pink-300"
            placeholder="you@example.com"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Password</label>
          <input
            v-model="form.password"
            type="password"
            required
            class="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-pink-300"
            placeholder="••••••••"
          />
        </div>

        <div v-if="error" class="text-red-500 text-sm bg-red-50 dark:bg-red-900/20 px-3 py-2 rounded-lg">{{ error }}</div>

        <button
          type="submit"
          :disabled="auth.loading"
          class="w-full py-2.5 bg-blue-500 text-white font-medium rounded-full hover:bg-pink-600 disabled:opacity-50 transition-colors"
        >
          {{ auth.loading ? 'Logging in...' : 'Login' }}
        </button>
      </form>

      <p class="text-center text-sm text-gray-500 dark:text-gray-400 mt-6">
        No account?
        <router-link to="/register" class="text-blue-500 hover:text-pink-600 font-medium">Sign up</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()
const form = ref({ 
  email: '',
  password: '' })
const error = ref('')

async function handleLogin() {
  error.value = ''
  try {
    await auth.login(form.value.email, form.value.password)
    router.push('/browse')
  } catch (e) {
    error.value = e.response?.data?.error || 'Login failed'
  }
}
</script>
