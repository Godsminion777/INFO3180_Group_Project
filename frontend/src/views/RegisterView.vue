<template>
  <div class="min-h-screen flex items-center justify-center bg-linear-to-br from-blue-100 to-pink-100 dark:from-blue-950 dark:to-pink-950 px-4 py-8">
    <div class="w-full max-w-lg bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8">
      <div class="text-center mb-6">
        <div class="text-4xl mb-2">🩵</div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100">Create Your Profile</h1>
      </div>

      <form @submit.prevent="handleRegister" class="space-y-4">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="field-label">First Name *</label>
            <input v-model="form.first_name" required class="field-input" placeholder="Jane" />
          </div>
          <div>
            <label class="field-label">Last Name *</label>
            <input v-model="form.last_name" required class="field-input" placeholder="Doe" />
          </div>
        </div>

        <div>
          <label class="field-label">Email *</label>
          <input v-model="form.email" type="email" required class="field-input" placeholder="you@example.com" />
          <p v-if="emailError" class="text-red-500 text-xs mt-1">{{ emailError }}</p>
        </div>

        <div>
          <label class="field-label">Username *</label>
          <input v-model="form.username" required class="field-input" placeholder="cooluser123" />
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="field-label">Password *</label>
            {Add password error handling}
            <input v-model="form.password" type="password" required class="field-input" placeholder="Must be 8-20 characters" />
          </div>
          <div>
            <label class="field-label">Age *</label>
            <input v-model.number="form.age" type="number" min="18" max="120" required class="field-input" />
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="field-label">Gender *</label>
            <select v-model="form.gender" required class="field-input">
              <option value="">Select...</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="non-binary">Non-binary</option>
              <option value="other">Other</option>
            </select>
          </div>
          <div>
            <label class="field-label">Looking For *</label>
            <select v-model="form.looking_for" required class="field-input">
              <option value="">Select...</option>
              <option value="male">Men</option>
              <option value="female">Women</option>
              <option value="any">Anyone</option>
            </select>
          </div>
        </div>

        <div>
          <label class="field-label">Location</label>
          <input v-model="form.location" class="field-input" placeholder="City, Country" />
        </div>

        <div>
          <label class="field-label">Occupation</label>
          <input v-model="form.occupation" class="field-input" placeholder="Software Engineer" />
        </div>

        <div>
          <label class="field-label">Relationship Goal</label>
          <select v-model="form.relationship_goal" class="field-input">
            <option value="">Select...</option>
            <option value="long-term">Long-term relationship</option>
            <option value="casual">Casual dating</option>
            <option value="friendship">Friendship</option>
            <option value="not-sure">Not sure yet</option>
          </select>
        </div>

        <div>
          <label class="field-label">Bio</label>
          <textarea v-model="form.bio" rows="3" class="field-input resize-none" placeholder="Tell people a little about yourself..."></textarea>
        </div>

        <div v-if="error" class="text-red-500 text-sm bg-red-50 dark:bg-red-900/20 px-3 py-2 rounded-lg">{{ error }}</div>

        <button
          type="submit"
          :disabled="auth.loading"
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
  first_name: '', last_name: '', email: '', username: '',
  password: '', age: 18, gender: '', looking_for: '',
  location: '', occupation: '', relationship_goal: '', bio: ''
})

const emailError = computed(() => {
  if (!form.value.email) return ''
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(form.value.email) ? '' : 'Invalid email address'
})

async function handleRegister() {
  if (emailError.value) return
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
