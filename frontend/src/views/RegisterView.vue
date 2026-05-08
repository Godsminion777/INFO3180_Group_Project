<template>
  <div class="register-page min-h-screen flex items-center justify-center bg-linear-to-br from-pink-200 to-blue-200 px-4 py-8">
    <div class="register-card w-full max-w-lg bg-white rounded-2xl shadow-xl p-8">
      <div class="text-center mb-6">
        <Logo size="xl"/>
        <h1 class="h1">Create Your Profile</h1>
      </div>

      <form @submit.prevent="handleRegister" class="space-y-4">
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label for="first-name" class="field-label">First Name *</label>
            <input id="first-name" v-model="form.first_name" required autocomplete="given-name" class="field-input" placeholder="Jane" />
          </div>
          <div>
            <label for="last-name" class="field-label">Last Name *</label>
            <input id="last-name" v-model="form.last_name" required autocomplete="family-name" class="field-input" placeholder="Doe" />
          </div>
        </div>

        <div>
          <label for="email" class="field-label">Email *</label>
          <input id="email" v-model="form.email" type="email" required autocomplete="email" class="field-input" placeholder="you@example.com" />
          <p v-if="emailError" class="text-red-500 text-xs mt-1">{{ emailError }}</p>
        </div>

        <div>
          <label for="username" class="field-label">Username *</label>
          <input id="username" v-model="form.username" required autocomplete="username" class="field-input" placeholder="cooluser123" />
          <p v-if="usernameError" class="text-red-500 text-xs mt-1">{{ usernameError }}</p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label for="password" class="field-label">Password *</label>
            <input id="password" v-model="form.password" type="password" required autocomplete="new-password" class="field-input" placeholder="Must be 8-20 characters" />
            <p v-if="passwordError" class="text-red-500 text-xs mt-1">{{ passwordError }}</p>
          </div>
          <div>
            <label for="age" class="field-label">Age *</label>
            <input id="age" v-model.number="form.age" type="number" min="18" max="120" required class="field-input" />
            <p v-if="ageError" class="text-red-500 text-xs mt-1">{{ ageError }}</p>
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label for="gender" class="field-label">Gender *</label>
            <select id="gender" v-model="form.gender" required class="field-input">
              <option value="">Select...</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="non-binary">Non-binary</option>
              <option value="other">Other</option>
            </select>
          </div>
          <div>
            <label for="looking-for" class="field-label">Looking For *</label>
            <select id="looking-for" v-model="form.looking_for" required class="field-input">
              <option value="">Select...</option>
              <option value="male">Men</option>
              <option value="female">Women</option>
              <option value="any">Anyone</option>
            </select>
          </div>
        </div>

        <div>
          <label for="location" class="field-label">Location</label>
          <input id="location" v-model="form.location" autocomplete="address-level2" class="field-input" placeholder="City, Country" />
        </div>

        <div>
          <label for="occupation" class="field-label">Occupation</label>
          <input id="occupation" v-model="form.occupation" autocomplete="organization-title" class="field-input" placeholder="Software Engineer" />
        </div>

        <div>
          <label for="relationship-goal" class="field-label">Relationship Goal</label>
          <select id="relationship-goal" v-model="form.relationship_goal" class="field-input">
            <option value="">Select...</option>
            <option value="long-term">Long-term relationship</option>
            <option value="casual">Casual dating</option>
            <option value="friendship">Friendship</option>
            <option value="not-sure">Not sure yet</option>
          </select>
        </div>

        <div>
          <label for="bio" class="field-label">Bio</label>
          <textarea id="bio" v-model="form.bio" rows="3" class="field-input resize-none" placeholder="Tell people a little about yourself..."></textarea>
        </div>

        <div v-if="error" class="text-red-500 text-sm bg-red-50 dark:bg-red-900/20 px-3 py-2 rounded-lg">{{ error }}</div>

        <button
          type="submit"
          :disabled="auth.loading"
          class="w-full py-3 text-base bg-blue-500 text-white font-medium rounded-full hover:bg-pink-500 disabled:opacity-50 transition-colors"
        >
          {{ auth.loading ? 'Creating account...' : 'Create Account' }}
        </button>
      </form>

      <p class="text-center text-sm text-gray-500 dark:text-gray-400 mt-4">
        Already have an account?
        <router-link to="/login" class="text-blue-500 hover:text-pink-500 font-medium">Login</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import Logo from '../components/Logo.vue'

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

const usernameError = computed(() => {
  if (!form.value.username) return ''
  if (form.value.username.length < 6) return 'Username must be at least 6 characters'
  if (form.value.username.length > 20) return 'Username must be 20 characters or fewer'
  if (!/^[a-zA-Z0-9_]+$/.test(form.value.username)) {
    return 'Username can only contain letters, numbers, and underscores'
  }
  return ''
})

const passwordError = computed(() => {
  if (!form.value.password) return ''
  if (form.value.password.length < 8) return 'Password must be 8-20 characters.'
  if (form.value.password.length > 20) return 'Password must be 8-20 characters.'
  return ''
})

const ageError = computed(() => {
  if (!form.value.age) return ''
  if (form.value.age < 18) return 'Users must be over 18 years old.'
  if (form.value.age > 120) return 'Users must be over 18 years old.'
  return ''
})

async function handleRegister() {
  if (emailError.value || usernameError.value || passwordError.value || ageError.value) return
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

.h1 {
  @apply text-2xl font-bold text-gray-900;
}

.field-label {
  @apply block text-sm font-medium text-blue-900 mb-1;
}

.field-input {
  @apply w-full px-3 py-3 border border-gray-300 rounded-lg bg-white text-base focus:outline-none focus:ring-2 focus:ring-pink-300;
}


@media (prefers-color-scheme: dark) {
  .register-page {
    @apply from-blue-950 to-pink-900;
  }
  .register-card {
    @apply bg-gray-800;
  }
  .h1 {
    @apply text-pink-100;
  }
  .field-label {
    @apply text-gray-300;
  }
  .field-input {
    @apply border-gray-600 bg-gray-700 focus:ring-pink-700;
  }
}

</style>