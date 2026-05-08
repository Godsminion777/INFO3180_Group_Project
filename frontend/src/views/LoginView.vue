<template>
  <div class="login-page min-h-screen flex items-center justify-center bg-linear-to-br from-pink-200 to-blue-200 px-4 py-8">
    <div class="login-card w-full max-w-md bg-white  rounded-2xl shadow-xl p-6">
      <div class="text-center mb-8">
        <Logo size="xl"/>
        <h1 class="h1">DriftDater</h1>
        <p class="text-gray-500 dark:text-gray-400 text-sm mt-1">🩵Go with the flow🩵</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label for="email" class="field-label">Email</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            required
            autocomplete="email"
            class="field-input"
            placeholder="you@example.com"
          />
        </div>

        <div>
          <label for="password" class="field-label">Password</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            required
            autocomplete="current-password"
            class="field-input"
            placeholder="••••••••"
          />
        </div>

        <div v-if="error" class="text-red-500 text-sm bg-red-50 dark:bg-red-900/20 px-3 py-2 rounded-lg">{{ error }}</div>

        <button
          type="submit"
          :disabled="auth.loading"
          class="w-full py-3 text-base bg-blue-500 text-white font-medium rounded-full hover:bg-pink-500 disabled:opacity-50 transition-colors"
        >
          {{ auth.loading ? 'Logging in...' : 'Login' }}
        </button>
      </form>

      <p class="text-center text-sm text-gray-500 dark:text-gray-400 mt-6">
        No account?
        <router-link to="/register" class="text-blue-500 hover:text-pink-500 font-medium">Sign up</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import Logo from '../components/Logo.vue'

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

<style scoped>
@reference "tailwindcss";

.h1 {
  @apply text-2xl font-bold text-gray-900;
}

.field-label {
  @apply block text-sm font-medium text-blue-900 mb-1;
}

.field-input {
  @apply w-full px-4 py-3 text-base border border-gray-300 rounded-lg bg-white text-base focus:outline-none focus:ring-2 focus:ring-pink-300;
}


@media (prefers-color-scheme: dark) {
  .login-page {
    @apply from-blue-950 to-pink-900;
  }
  .login-card {
    @apply bg-gray-800;
  }
  .h1 {
    @apply text-gray-100;
  }
  .field-label {
    @apply text-gray-300;
  }
  .field-input {
    @apply border-gray-600 bg-gray-700 focus:ring-pink-700;
  }
}

</style>