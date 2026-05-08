<template>
  <div class="min-h-screen bg-linear-to-br from-pink-200 to-blue-200 dark:from-blue-950 dark:to-pink-950">
    <div class="max-w-5xl mx-auto px-4 py-8">
      <h1 class="text-2xl font-bold mb-6 text-gray-900 dark:text-gray-100">Search & Discover</h1>

      <!-- Filter form -->
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-5 mb-6">
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 mb-4">
          <div>
            <label for="search-location" class="field-label">Location</label>
            <input id="search-location" v-model="filters.location" autocomplete="address-level2" class="field-input" placeholder="City, Country" />
          </div>
          <div>
            <label for="search-age-min" class="field-label">Min Age</label>
            <input id="search-age-min" v-model.number="filters.ageMin" type="number" min="18" class="field-input" />
          </div>
          <div>
            <label for="search-age-max" class="field-label">Max Age</label>
            <input id="search-age-max" v-model.number="filters.ageMax" type="number" max="120" class="field-input" />
          </div>
          <div>
            <label for="search-keyword" class="field-label">Keyword</label>
            <input id="search-keyword" v-model="filters.keyword" class="field-input" placeholder="Name, bio..." />
          </div>
        </div>

        <div class="flex flex-col sm:flex-row gap-3 sm:gap-4 sm:items-end">
          <div class="flex-1">
            <label for="search-interest" class="field-label">Interests (any match)</label>
            <input id="search-interest" v-model="interestInput" class="field-input" placeholder="e.g. hiking, music" @keydown.enter.prevent="addInterest" />
          </div>
          <button type="button" @click="addInterest" class="px-4 py-3 bg-pink-500 text-white rounded-lg text-base hover:bg-pink-600">Add</button>
        </div>

        <div v-if="filters.interests.length" class="flex flex-wrap gap-2 mt-3">
          <span v-for="i in filters.interests" :key="i"
            class="flex items-center gap-1 px-2 py-0.5 bg-pink-50 dark:bg-pink-900/30 text-pink-600 dark:text-pink-300 rounded-full text-xs">
            {{ i }}
            <button @click="removeInterest(i)" aria-label="Remove interest" class="font-bold hover:text-red-500 px-1">×</button>
          </span>
        </div>

        <!-- Sort options -->
        <div class="flex flex-wrap items-center gap-3 sm:gap-4 mt-4 pt-4 border-t border-gray-100 dark:border-gray-700">
          <span class="text-sm font-medium text-gray-600 dark:text-gray-400">Sort by:</span>
          <label v-for="opt in sortOptions" :key="opt.value" class="flex items-center gap-1 cursor-pointer">
            <input type="radio" v-model="sortBy" :value="opt.value" class="text-pink-500" />
            <span class="text-sm text-gray-600 dark:text-gray-300">{{ opt.label }}</span>
          </label>
          <button @click="clearFilters" class="ml-auto text-sm text-gray-400 hover:text-gray-600 dark:hover:text-gray-200">Clear all</button>
        </div>
      </div>

      <!-- Results count -->
      <p class="text-sm text-gray-500 dark:text-gray-400 mb-4">{{ results.length }} profile{{ results.length !== 1 ? 's' : '' }} found</p>

      <!-- Results grid -->
      <div v-if="results.length" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        <router-link
          v-for="profile in results"
          :key="profile.id"
          :to="`/profile/${profile.user_id}`"
        >
          <ProfileCard :profile="profile" :is-saved="profilesStore.isSaved(profile.id)" @save="profilesStore.toggleSave(profile.id)" />
        </router-link>
      </div>

      <div v-else-if="profilesStore.allProfiles.length === 0 && !loading" class="text-center py-20 text-gray-400">
        <p>Loading profiles...</p>
      </div>

      <div v-else class="text-center py-20">
        <div class="text-5xl mb-4">🔍</div>
        <p class="text-gray-500">No profiles match your search</p>
        <button @click="clearFilters" class="mt-3 text-sm text-pink-500 hover:underline">Clear filters</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useProfilesStore } from '../stores/profiles'
import ProfileCard from '../components/ProfileCard.vue'

const profilesStore = useProfilesStore()
const loading = ref(false)
const interestInput = ref('')
const sortBy = ref('newest')

const filters = ref({
  location: '', ageMin: '', ageMax: '', keyword: '', interests: []
})

const sortOptions = [
  { value: 'newest', label: 'Newest' },
  { value: 'oldest', label: 'Oldest' },
  { value: 'age-asc', label: 'Age ↑' },
  { value: 'age-desc', label: 'Age ↓' }
]

const results = computed(() => {
  let list = profilesStore.searchProfiles(filters.value)
  if (sortBy.value === 'newest') list = [...list].sort((a, b) => b.id - a.id)
  else if (sortBy.value === 'oldest') list = [...list].sort((a, b) => a.id - b.id)
  else if (sortBy.value === 'age-asc') list = [...list].sort((a, b) => a.age - b.age)
  else if (sortBy.value === 'age-desc') list = [...list].sort((a, b) => b.age - a.age)
  return list
})

function addInterest() {
  const val = interestInput.value.trim().toLowerCase()
  if (val && !filters.value.interests.includes(val)) {
    filters.value.interests.push(val)
  }
  interestInput.value = ''
}

function removeInterest(i) {
  filters.value.interests = filters.value.interests.filter(x => x !== i)
}

function clearFilters() {
  filters.value = { location: '', ageMin: '', ageMax: '', keyword: '', interests: [] }
  sortBy.value = 'newest'
}

onMounted(async () => {
  if (!profilesStore.allProfiles.length) {
    loading.value = true
    await profilesStore.fetchAll()
    loading.value = false
  }
})
</script>

<style scoped>
@reference "tailwindcss";
@custom-variant dark (&:where(.dark, .dark *));
.field-label { @apply block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1; }
.field-input { @apply w-full px-3 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-base focus:outline-none focus:ring-2 focus:ring-pink-300; }
</style>