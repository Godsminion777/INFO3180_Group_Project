<template>
  <div class="max-w-5xl mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold mb-6 text-gray-900 dark:text-gray-100">Your Matches 💕</h1>

    <div v-if="loading" class="text-center py-20 text-gray-400">Loading...</div>

    <div v-else-if="profiles.length === 0" class="text-center py-20">
      <div class="text-5xl mb-4">💫</div>
      <p class="text-lg text-gray-500">No mutual matches yet</p>
      <p class="text-sm text-gray-400 mt-1">Keep liking people and you'll match soon!</p>
      <router-link to="/browse" class="mt-4 inline-block px-6 py-2 bg-pink-500 text-white rounded-full hover:bg-pink-600">
        Browse People
      </router-link>
    </div>

    <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      <div
        v-for="item in profiles"
        :key="item.match.id"
        class="bg-white dark:bg-gray-800 rounded-xl overflow-hidden shadow hover:shadow-md transition-shadow cursor-pointer"
      >
        <div class="relative h-40 bg-gradient-to-br from-pink-100 to-purple-100 dark:from-pink-900/30 dark:to-purple-900/30">
          <img
            v-if="item.profile?.photo_url"
            :src="item.profile.photo_url"
            class="w-full h-full object-cover"
          />
          <div v-else class="w-full h-full flex items-center justify-center text-4xl">👤</div>
          <div v-if="item.match.action === 'superlike'" class="absolute top-2 right-2 text-lg">⭐</div>
        </div>
        <div class="p-3">
          <p class="font-semibold text-sm text-gray-900 dark:text-gray-100">
            {{ item.profile?.first_name || 'Unknown' }}
          </p>
          <p class="text-xs text-gray-400 mb-2">{{ item.profile?.location || '' }}</p>
          <div class="flex gap-2">
            <router-link
              v-if="item.profile"
              :to="`/profile/${item.profile.id}`"
              class="flex-1 text-center text-xs py-1.5 border border-pink-300 text-pink-500 rounded-full hover:bg-pink-50 dark:hover:bg-pink-900/20"
            >
              Profile
            </router-link>
            <router-link
              :to="`/messages/${item.otherUserId}`"
              class="flex-1 text-center text-xs py-1.5 bg-pink-500 text-white rounded-full hover:bg-pink-600"
            >
              Chat
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useMatchesStore } from '../stores/matches'
import { useProfilesStore } from '../stores/profiles'
import { useAuthStore } from '../stores/auth'

const matchesStore = useMatchesStore()
const profilesStore = useProfilesStore()
const auth = useAuthStore()
const loading = ref(false)
const profiles = ref([])

onMounted(async () => {
  loading.value = true
  await matchesStore.fetchMutual()
  const enriched = await Promise.all(
    matchesStore.mutualMatches.map(async match => {
      const currentUserId = auth.user?.id
      const otherUserId = match.sender_id === currentUserId ? match.receiver_id : match.sender_id
      try {
        const profile = await profilesStore.fetchOneByUserId(otherUserId)
        return { match, profile, otherUserId }
      } catch {
        return { match, profile: null, otherUserId }
      }
    })
  )
  profiles.value = enriched
  loading.value = false
})
</script>
