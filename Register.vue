<template>
  <div class="min-h-screen flex items-center justify-center bg-linear-to-br from-blue-100 to-pink-100 dark:from-blue-950 dark:to-pink-950 px-4 py-8">
    <div class="w-full max-w-md bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8">
      <div class="text-center mb-6">
        <div class="text-4xl mb-2">🩵</div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100">Create Your Account</h1>
        <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">You can complete your profile after signing up.</p>
      </div>

      <form @submit.prevent="handleRegister" class="space-y-4">
        <div>
          <label for="username" class="field-label">Username *</label>
          <input
            id="username"
            v-model="form.username"
            required
            autocomplete="username"
            class="field-input"
            placeholder="cooluser123"
          />
          <p v-if="usernameError" class="text-red-500 text-xs mt-1">{{ usernameError }}</p>
        </div>

        <div>
          <label for="email" class="field-label">Email *</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            required
            autocomplete="email"
            class="field-input"
            placeholder="you@example.com"
          />
          <p v-if="emailError" class="text-red-500 text-xs mt-1">{{ emailError }}</p>
        </div>

        <div>
          <label for="password" class="field-label">Password *</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            required
            autocomplete="new-password"
            class="field-input"
            placeholder="Must be 8-20 characters"
          />
          <p v-if="passwordError" class="text-red-500 text-xs mt-1">{{ passwordError }}</p>
        </div>

        <div v-if="error" class="text-red-500 text-sm bg-red-50 dark:bg-red-900/20 px-3 py-2 rounded-lg">
          {{ error }}
        </div>

        <button
          type="submit"
          :disabled="auth.loading || hasErrors"
          class="w-full py-2.5 bg-blue-500 text-white font-medium rounded-full hover:bg-pink-700 disabled:opacity-50 transition-colors"
        >
          {{ auth.loading ? 'Creating account...' : 'Create Account' }}
        </button>
      </form>

      <p class="text-center text-sm text-gray-500 dark:text-gray-400 mt-4">
        Already have an account?
        <router-link to="/login" class="text-blue-500 hover:text-pink-600 font-medium">Login</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()
const error = ref('')

const form = ref({
  username: '',
  email: '',
  password: '',
})

const usernameError = computed(() => {
  if (!form.value.username) return ''
  if (form.value.username.length < 6) return 'Username must be at least 6 characters'
  if (form.value.username.length > 20) return 'Username must be 20 characters or fewer'
  if (!/^[a-zA-Z0-9_]+$/.test(form.value.username)) {
    return 'Username can only contain letters, numbers, and underscores'
  }
  return ''
})

const emailError = computed(() => {
  if (!form.value.email) return ''
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(form.value.email) ? '' : 'Invalid email address'
})

const passwordError = computed(() => {
  if (!form.value.password) return ''
  if (form.value.password.length < 8) return 'Password must be at least 8 characters'
  if (form.value.password.length > 20) return 'Password must be 20 characters or fewer'
  return ''
})

const hasErrors = computed(() =>
  !!usernameError.value || !!emailError.value || !!passwordError.value
)

async function handleRegister() {
  if (hasErrors.value) return
  error.value = ''
  try {
    await auth.register(form.value)
    router.push(`/profile/${auth.user.id}/edit`)
  } catch (e) {
    error.value = e.response?.data?.error || 'Registration failed'
  }
}
</script>

<style scoped>
@reference "tailwindcss";
.field-label {
  @apply block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1;
}
.field-input {
  @apply w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-sm focus:outline-none focus:ring-2 focus:ring-pink-300;
}
</style>