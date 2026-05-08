<template>
  <div class="min-h-screen bg-linear-to-br from-pink-200 to-blue-200 dark:from-blue-950 dark:to-pink-950">
    <div class="max-w-2xl mx-auto px-4 py-8">
      <div v-if="loading" class="text-center py-20 text-gray-400">Loading...</div>
      <div v-else-if="profile" class="bg-white dark:bg-gray-800 rounded-2xl shadow-lg overflow-hidden">
        <!-- Cover/Photo -->
        <div class="relative h-64 bg-gradient-to-br from-pink-200 to-purple-200 dark:from-pink-900/40 dark:to-purple-900/40">
          <img
            v-if="profile.photo_url"
            :src="profile.photo_url"
            class="w-full h-full object-cover"
            :alt="profile.first_name"
          />
          <div v-else class="w-full h-full flex items-center justify-center text-8xl">👤</div>

          <div v-if="isOwnProfile" class="absolute top-4 right-4">
            <router-link :to="`/profile/${profile.id}/edit`" class="px-4 py-2 bg-white/90 dark:bg-gray-800/90 rounded-full text-sm font-medium hover:bg-white">
              Edit
            </router-link>
          </div>
        </div>

        <div class="p-6">
          <div class="flex items-start justify-between gap-3 mb-4">
            <div class="min-w-0">
              <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100">
                {{ profile.first_name }} {{ profile.last_name }}
                <span v-if="!profile.is_public" class="ml-2 text-xs bg-gray-200 dark:bg-gray-700 text-gray-500 px-2 py-0.5 rounded-full">Private</span>
              </h1>
              <p class="text-gray-500 dark:text-gray-400">{{ profile.age }} years old</p>
            </div>
            <button
              v-if="!isOwnProfile"
              @click="profilesStore.toggleSave(profile.id)"
              :aria-label="profilesStore.isSaved(profile.id) ? 'Unsave profile' : 'Save profile'"
              class="text-3xl p-2 hover:scale-110 transition-transform flex-shrink-0"
            >
              {{ profilesStore.isSaved(profile.id) ? '❤️' : '🤍' }}
            </button>
          </div>

          <div v-if="profile.location" class="flex items-center gap-1 text-gray-500 dark:text-gray-400 text-sm mb-4">
            <span>📍</span>
            <span>{{ profile.location }}</span>
          </div>

          <div v-if="profile.bio" class="mb-6">
            <h3 class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">About</h3>
            <p class="text-gray-600 dark:text-gray-300">{{ profile.bio }}</p>
          </div>

          <!-- Details grid -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
            <div v-if="profile.occupation" class="bg-gray-50 dark:bg-gray-700 rounded-lg p-3">
              <p class="text-xs text-gray-400 mb-1">Occupation</p>
              <p class="text-sm font-medium">💼 {{ profile.occupation }}</p>
            </div>
            <div v-if="profile.education" class="bg-gray-50 dark:bg-gray-700 rounded-lg p-3">
              <p class="text-xs text-gray-400 mb-1">Education</p>
              <p class="text-sm font-medium">🎓 {{ profile.education }}</p>
            </div>
            <div v-if="profile.relationship_goal" class="bg-gray-50 dark:bg-gray-700 rounded-lg p-3">
              <p class="text-xs text-gray-400 mb-1">Looking For</p>
              <p class="text-sm font-medium">🎯 {{ profile.relationship_goal }}</p>
            </div>
            <div v-if="profile.looking_for" class="bg-gray-50 dark:bg-gray-700 rounded-lg p-3">
              <p class="text-xs text-gray-400 mb-1">Interested In</p>
              <p class="text-sm font-medium">💕 {{ profile.looking_for }}</p>
            </div>
          </div>

          <!-- Interests -->
          <div v-if="profile.interests?.length" class="mb-6">
            <h3 class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">Interests</h3>
            <div class="flex flex-wrap gap-2">
              <span v-for="i in profile.interests" :key="i"
                class="px-3 py-1 bg-pink-50 dark:bg-pink-900/30 text-pink-600 dark:text-pink-300 rounded-full text-sm">
                {{ i }}
              </span>
            </div>
          </div>

          <!-- Action buttons for non-own profiles -->
          <div v-if="!isOwnProfile" class="flex flex-col sm:flex-row gap-3">
            <button @click="doAct('like')" class="flex-1 py-3 text-base bg-pink-500 text-white rounded-full font-medium hover:bg-pink-600">
              ❤️ Like
            </button>
            <button @click="doAct('superlike')" class="flex-1 sm:flex-initial sm:px-6 py-3 text-base bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-300 rounded-full font-medium hover:bg-blue-100 dark:hover:bg-blue-900/50">
              ⭐ Super
            </button>
            <button @click="doAct('dislike')" class="flex-1 sm:flex-initial sm:px-6 py-3 text-base bg-gray-100 dark:bg-gray-700 rounded-full font-medium hover:bg-gray-200 dark:hover:bg-gray-600">
              👎 Pass
            </button>
          </div>
        </div>
      </div>
      <div v-else class="text-center py-20 text-gray-400">Profile not found.</div>
    </div>
  </div>

  <MatchModal
    :show="!!matches.newMatchAlert"
    :match-name="matchNameStr"
    @close="matches.clearAlert()"
    @message="goMsg()"
  />
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useProfilesStore } from '../stores/profiles'
import { useMatchesStore } from '../stores/matches'
import { useUiStore } from '../stores/ui'
import MatchModal from '../components/MatchModal.vue'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const profilesStore = useProfilesStore()
const matches = useMatchesStore()
const ui = useUiStore()

const profile = ref(null)
const loading = ref(false)

const isOwnProfile = computed(() => auth.user?.id === profile.value?.user_id)
const matchNameStr = computed(() => profile.value?.first_name || '')

async function doAct(action) {
  try {
    const res = await matches.act(profile.value.user_id, action)
    if (res.match?.is_mutual) {
      ui.notify(`It's a match! 💕`, 'match')
    } else if (action === 'like') {
      ui.notify('Liked!', 'success')
    }
  } catch (e) {
    ui.notify(e.response?.data?.error || 'Failed', 'error')
  }
}

function goMsg() {
  const alert = matches.newMatchAlert
  if (alert) {
    matches.clearAlert()
    router.push(`/messages/${alert.receiver_id}`)
  }
}

onMounted(async () => {
  loading.value = true
  try {
    profile.value = await profilesStore.fetchOne(route.params.id)
  } catch {
    profile.value = null
  }
  loading.value = false
})
</script>