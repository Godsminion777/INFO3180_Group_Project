<template>
  <div class="max-w-5xl mx-auto px-4 py-8">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100">Discover People</h1>
      <div class="flex items-center gap-3">
        <select v-model="sortBy" class="text-sm border border-gray-300 dark:border-gray-600 rounded-lg px-3 py-1.5 bg-white dark:bg-gray-700 focus:outline-none">
          <option value="score">Best Match</option>
          <option value="newest">Newest</option>
          <option value="age">By Age</option>
        </select>
        <button @click="showFilters = !showFilters" class="flex items-center gap-1 text-sm px-3 py-1.5 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700">
          🔧 Filter
        </button>
      </div>
    </div>

    <!-- Filters panel -->
    <div v-if="showFilters" class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl p-4 mb-6 grid grid-cols-2 md:grid-cols-4 gap-4">
      <div>
        <label class="text-xs font-medium text-gray-600 dark:text-gray-400">Min Age</label>
        <input v-model.number="filters.ageMin" type="number" min="18" max="100" class="filter-input" />
      </div>
      <div>
        <label class="text-xs font-medium text-gray-600 dark:text-gray-400">Max Age</label>
        <input v-model.number="filters.ageMax" type="number" min="18" max="100" class="filter-input" />
      </div>
      <div>
        <label class="text-xs font-medium text-gray-600 dark:text-gray-400">Location</label>
        <input v-model="filters.location" type="text" placeholder="City..." class="filter-input" />
      </div>
      <div>
        <label class="text-xs font-medium text-gray-600 dark:text-gray-400">Interest</label>
        <input v-model="filters.interest" type="text" placeholder="e.g. hiking" class="filter-input" />
      </div>
    </div>

    <!-- Swipe card (top candidate) -->
    <div v-if="currentCandidate" class="flex flex-col items-center mb-10">
      <div class="relative w-full max-w-sm bg-white dark:bg-gray-800 rounded-2xl shadow-xl overflow-hidden">
        <div class="relative h-72 bg-gradient-to-br from-pink-100 to-purple-100 dark:from-pink-900/30 dark:to-purple-900/30">
          <img
            v-if="currentCandidate.profile.photo_url"
            :src="currentCandidate.profile.photo_url"
            class="w-full h-full object-cover"
            :alt="currentCandidate.profile.first_name"
          />
          <div v-else class="w-full h-full flex items-center justify-center text-7xl">👤</div>
          <div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/70 to-transparent p-4">
            <h2 class="text-white text-xl font-bold">{{ currentCandidate.profile.first_name }}, {{ currentCandidate.profile.age }}</h2>
            <p class="text-white/80 text-sm">📍 {{ currentCandidate.profile.location || 'Location unknown' }}</p>
          </div>
          <div class="absolute top-3 right-3 bg-pink-500 text-white px-2 py-1 rounded-full text-xs font-medium">
            {{ currentCandidate.match_score }}% match
          </div>
        </div>
        <div class="p-4">
          <p v-if="currentCandidate.profile.bio" class="text-gray-600 dark:text-gray-300 text-sm mb-3">{{ currentCandidate.profile.bio }}</p>
          <div class="flex flex-wrap gap-1 mb-3">
            <span v-for="i in (currentCandidate.profile.interests || []).slice(0, 5)" :key="i"
              class="text-xs px-2 py-0.5 bg-pink-50 dark:bg-pink-900/30 text-pink-600 dark:text-pink-300 rounded-full">
              {{ i }}
            </span>
          </div>
          <router-link :to="`/profile/${currentCandidate.profile.id}`" class="text-xs text-pink-500 hover:underline">View full profile →</router-link>
        </div>
      </div>

      <!-- Action buttons -->
      <div class="flex items-center gap-6 mt-6">
        <button @click="doAct('dislike')" class="w-14 h-14 bg-white dark:bg-gray-700 rounded-full shadow-md flex items-center justify-center text-2xl hover:scale-110 transition-transform border border-gray-100 dark:border-gray-600">
          👎
        </button>
        <button @click="doAct('superlike')" class="w-12 h-12 bg-blue-50 dark:bg-blue-900/30 rounded-full shadow-md flex items-center justify-center text-xl hover:scale-110 transition-transform border border-blue-100 dark:border-blue-700">
          ⭐
        </button>
        <button @click="doAct('like')" class="w-14 h-14 bg-pink-500 rounded-full shadow-md flex items-center justify-center text-2xl hover:scale-110 transition-transform">
          ❤️
        </button>
      </div>
    </div>

    <div v-else-if="!loading" class="text-center py-20 text-gray-400">
      <div class="text-5xl mb-4">🎉</div>
      <p class="text-lg">You've seen everyone for now!</p>
      <p class="text-sm mt-1">Check back later for new people.</p>
    </div>

    <div v-if="loading" class="text-center py-20 text-gray-400">Loading...</div>

    <!-- More profiles grid -->
    <div v-if="remaining.length > 0">
      <h2 class="text-lg font-semibold mb-4 text-gray-800 dark:text-gray-200">More People</h2>
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        <router-link
          v-for="pm in remaining"
          :key="pm.profile.id"
          :to="`/profile/${pm.profile.id}`"
          class="bg-white dark:bg-gray-800 rounded-xl overflow-hidden shadow hover:shadow-md transition-shadow"
        >
          <div class="h-32 bg-gradient-to-br from-pink-100 to-purple-100 dark:from-pink-900/30 dark:to-purple-900/30 flex items-center justify-center">
            <img v-if="pm.profile.photo_url" :src="pm.profile.photo_url" class="w-full h-full object-cover" />
            <span v-else class="text-4xl">👤</span>
          </div>
          <div class="p-3">
            <p class="font-medium text-sm">{{ pm.profile.first_name }}, {{ pm.profile.age }}</p>
            <p class="text-xs text-gray-500">{{ pm.profile.location }}</p>
          </div>
        </router-link>
      </div>
    </div>
  </div>

  <MatchModal
    :show="!!matches.newMatchAlert"
    :match-name="matchName"
    @close="matches.clearAlert()"
    @message="goMessage()"
  />
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useMatchesStore } from '../stores/matches'
import { useUiStore } from '../stores/ui'
import MatchModal from '../components/MatchModal.vue'

const matches = useMatchesStore()
const ui = useUiStore()
const router = useRouter()
const loading = ref(false)
const showFilters = ref(false)
const sortBy = ref('score')
const filters = ref({ ageMin: '', ageMax: '', location: '', interest: '' })

const filtered = computed(() => {
  let list = [...matches.potentialMatches]
  const f = filters.value
  if (f.ageMin) list = list.filter(pm => pm.profile.age >= f.ageMin)
  if (f.ageMax) list = list.filter(pm => pm.profile.age <= f.ageMax)
  if (f.location) list = list.filter(pm => pm.profile.location?.toLowerCase().includes(f.location.toLowerCase()))
  if (f.interest) list = list.filter(pm => pm.profile.interests?.some(i => i.toLowerCase().includes(f.interest.toLowerCase())))
  if (sortBy.value === 'newest') list.sort((a, b) => b.profile.id - a.profile.id)
  else if (sortBy.value === 'age') list.sort((a, b) => a.profile.age - b.profile.age)
  return list
})

const currentCandidate = computed(() => filtered.value[0] || null)
const remaining = computed(() => filtered.value.slice(1))
const matchName = computed(() => {
  const alert = matches.newMatchAlert
  if (!alert) return ''
  const pm = matches.potentialMatches.find(p => p.profile.user_id === alert.receiver_id)
  return pm?.profile.first_name || 'Someone'
})

async function doAct(action) {
  if (!currentCandidate.value) return
  const receiverId = currentCandidate.value.profile.user_id
  try {
    const res = await matches.act(receiverId, action)
    if (res.match?.is_mutual) {
      ui.notify(`It's a match with ${currentCandidate.value?.profile.first_name}! 💕`, 'match')
    }
  } catch (e) {
    ui.notify('Action failed', 'error')
  }
}

function goMessage() {
  const alert = matches.newMatchAlert
  if (alert) {
    matches.clearAlert()
    router.push(`/messages/${alert.receiver_id}`)
  }
}

onMounted(async () => {
  loading.value = true
  await matches.fetchPotential()
  loading.value = false
})
</script>

<style scoped>
@reference "tailwindcss";
.filter-input {
  @apply w-full mt-1 px-2 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 focus:outline-none focus:ring-1 focus:ring-pink-300;
}
</style>
