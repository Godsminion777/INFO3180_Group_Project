<template>
  <div class="max-w-2xl mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold mb-6 text-gray-900 dark:text-gray-100">Edit Profile</h1>

    <div v-if="loading" class="text-center py-20 text-gray-400">Loading...</div>

    <form v-else @submit.prevent="handleSave" class="space-y-5">
      <!-- Photo upload -->
      <div class="bg-white dark:bg-gray-800 rounded-xl p-5 shadow-sm">
        <h2 class="font-semibold mb-4">Profile Photo</h2>
        <div class="flex items-center gap-4">
          <div class="w-20 h-20 rounded-full bg-gradient-to-br from-pink-100 to-purple-100 dark:from-pink-900/30 dark:to-purple-900/30 overflow-hidden flex items-center justify-center text-3xl">
            <img v-if="previewUrl || form.photo_url" :src="previewUrl || form.photo_url" class="w-full h-full object-cover" />
            <span v-else>👤</span>
          </div>
          <div>
            <input type="file" accept="image/*" @change="onFileChange" class="hidden" ref="fileInput" />
            <button type="button" @click="fileInput.click()" class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm hover:bg-gray-50 dark:hover:bg-gray-700">
              Upload Photo
            </button>
            <p class="text-xs text-gray-400 mt-1">PNG, JPG, GIF up to 5MB</p>
          </div>
        </div>
      </div>

      <!-- Basic info -->
      <div class="bg-white dark:bg-gray-800 rounded-xl p-5 shadow-sm">
        <h2 class="font-semibold mb-4">Basic Info</h2>
        <div class="grid grid-cols-2 gap-4 mb-4">
          <div>
            <label class="field-label">First Name</label>
            <input v-model="form.first_name" class="field-input" />
          </div>
          <div>
            <label class="field-label">Last Name</label>
            <input v-model="form.last_name" class="field-input" />
          </div>
        </div>
        <div class="grid grid-cols-2 gap-4 mb-4">
          <div>
            <label class="field-label">Age</label>
            <input v-model.number="form.age" type="number" min="18" class="field-input" />
          </div>
          <div>
            <label class="field-label">Gender</label>
            <select v-model="form.gender" class="field-input">
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="non-binary">Non-binary</option>
              <option value="other">Other</option>
            </select>
          </div>
        </div>
        <div>
          <label class="field-label">Bio</label>
          <textarea v-model="form.bio" rows="4" class="field-input resize-none"></textarea>
        </div>
      </div>

      <!-- Location & Preferences -->
      <div class="bg-white dark:bg-gray-800 rounded-xl p-5 shadow-sm">
        <h2 class="font-semibold mb-4">Location & Preferences</h2>
        <div class="grid grid-cols-2 gap-4 mb-4">
          <div>
            <label class="field-label">Location</label>
            <input v-model="form.location" class="field-input" placeholder="City, Country" />
          </div>
          <div>
            <label class="field-label">Looking For</label>
            <select v-model="form.looking_for" class="field-input">
              <option value="male">Men</option>
              <option value="female">Women</option>
              <option value="any">Anyone</option>
            </select>
          </div>
        </div>
        <div class="grid grid-cols-3 gap-4">
          <div>
            <label class="field-label">Min Age Pref</label>
            <input v-model.number="form.preferred_age_min" type="number" min="18" class="field-input" />
          </div>
          <div>
            <label class="field-label">Max Age Pref</label>
            <input v-model.number="form.preferred_age_max" type="number" max="120" class="field-input" />
          </div>
          <div>
            <label class="field-label">Distance (km)</label>
            <input v-model.number="form.distance_preference_km" type="number" min="1" class="field-input" />
          </div>
        </div>
      </div>

      <!-- Additional fields -->
      <div class="bg-white dark:bg-gray-800 rounded-xl p-5 shadow-sm">
        <h2 class="font-semibold mb-4">Additional Info</h2>
        <div class="grid grid-cols-2 gap-4 mb-4">
          <div>
            <label class="field-label">Occupation</label>
            <input v-model="form.occupation" class="field-input" placeholder="Job title" />
          </div>
          <div>
            <label class="field-label">Education</label>
            <input v-model="form.education" class="field-input" placeholder="Degree / School" />
          </div>
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
      </div>

      <!-- Interests -->
      <div class="bg-white dark:bg-gray-800 rounded-xl p-5 shadow-sm">
        <h2 class="font-semibold mb-4">Interests <span class="text-xs font-normal text-gray-400">(minimum 3)</span></h2>
        <InterestInput v-model="form.interests" />
        <p v-if="form.interests.length < 3" class="text-yellow-500 text-xs mt-2">⚠️ Add at least 3 interests</p>
      </div>

      <!-- Visibility -->
      <div class="bg-white dark:bg-gray-800 rounded-xl p-5 shadow-sm flex items-center justify-between">
        <div>
          <h2 class="font-semibold">Profile Visibility</h2>
          <p class="text-sm text-gray-500 dark:text-gray-400">Control who can see your profile</p>
        </div>
        <label class="relative inline-flex items-center cursor-pointer">
          <input type="checkbox" v-model="form.is_public" class="sr-only" />
          <div class="w-11 h-6 rounded-full transition-colors" :class="form.is_public ? 'bg-pink-500' : 'bg-gray-300 dark:bg-gray-600'">
            <div class="w-5 h-5 bg-white rounded-full shadow transform transition-transform mt-0.5 ml-0.5" :class="form.is_public ? 'translate-x-5' : 'translate-x-0'"></div>
          </div>
          <span class="ml-2 text-sm text-gray-600 dark:text-gray-300">{{ form.is_public ? 'Public' : 'Private' }}</span>
        </label>
      </div>

      <div v-if="error" class="text-red-500 text-sm bg-red-50 dark:bg-red-900/20 px-3 py-2 rounded-lg">{{ error }}</div>

      <div class="flex gap-3">
        <button type="submit" :disabled="saving || form.interests.length < 3" class="flex-1 py-3 bg-pink-500 text-white rounded-full font-medium hover:bg-pink-600 disabled:opacity-50">
          {{ saving ? 'Saving...' : 'Save Profile' }}
        </button>
        <router-link :to="`/profile/${route.params.id}`" class="px-6 py-3 border border-gray-300 dark:border-gray-600 rounded-full text-center hover:bg-gray-50 dark:hover:bg-gray-700">
          Cancel
        </router-link>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useProfilesStore } from '../stores/profiles'
import { useUiStore } from '../stores/ui'
import InterestInput from '../components/InterestInput.vue'

const route = useRoute()
const router = useRouter()
const profilesStore = useProfilesStore()
const ui = useUiStore()

const loading = ref(false)
const saving = ref(false)
const error = ref('')
const fileInput = ref(null)
const previewUrl = ref('')
const pendingFile = ref(null)

const form = ref({
  first_name: '', last_name: '', age: 18, bio: '', gender: '',
  looking_for: '', location: '', latitude: null, longitude: null,
  preferred_age_min: 18, preferred_age_max: 100, distance_preference_km: 50,
  occupation: '', education: '', relationship_goal: '',
  is_public: true, photo_url: '', interests: []
})

function onFileChange(e) {
  const file = e.target.files[0]
  if (!file) return
  pendingFile.value = file
  previewUrl.value = URL.createObjectURL(file)
}

async function handleSave() {
  saving.value = true
  error.value = ''
  try {
    const { photo_url, ...data } = form.value
    await profilesStore.update(route.params.id, data)

    if (pendingFile.value) {
      await profilesStore.uploadPhoto(route.params.id, pendingFile.value)
    }

    ui.notify('Profile saved!', 'success')
    router.push(`/profile/${route.params.id}`)
  } catch (e) {
    error.value = e.response?.data?.error || 'Failed to save'
  }
  saving.value = false
}

onMounted(async () => {
  loading.value = true
  const profile = await profilesStore.fetchOne(route.params.id)
  if (profile) {
    Object.keys(form.value).forEach(key => {
      if (profile[key] !== undefined && profile[key] !== null) {
        form.value[key] = profile[key]
      }
    })
  }
  loading.value = false
})
</script>

<style scoped>
@reference "tailwindcss";
.field-label { @apply block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1; }
.field-input { @apply w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-sm focus:outline-none focus:ring-2 focus:ring-pink-300; }
</style>
