<template>
  <div class="max-w-5xl mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold mb-6 text-gray-900 dark:text-gray-100">Saved Profiles ❤️</h1>

    <div v-if="loading" class="text-center py-20 text-gray-400">Loading...</div>

    <div v-else-if="profilesStore.savedProfiles.length === 0" class="text-center py-20">
      <div class="text-5xl mb-4">🤍</div>
      <p class="text-gray-500">No saved profiles yet</p>
      <p class="text-sm text-gray-400 mt-1">Tap the heart icon on any profile to save it here.</p>
      <router-link to="/search" class="mt-4 inline-block px-6 py-2 bg-pink-500 text-white rounded-full hover:bg-pink-600">
        Discover People
      </router-link>
    </div>

    <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      <router-link
        v-for="profile in profilesStore.savedProfiles"
        :key="profile.id"
        :to="`/profile/${profile.user_id}`"
      >
        <ProfileCard
          :profile="profile"
          :is-saved="true"
          @save="profilesStore.toggleSave(profile.id)"
        />
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useProfilesStore } from '../stores/profiles'
import ProfileCard from '../components/ProfileCard.vue'

const profilesStore = useProfilesStore()
const loading = ref(false)

onMounted(async () => {
  if (!profilesStore.allProfiles.length) {
    loading.value = true
    await profilesStore.fetchAll()
    loading.value = false
  }
})
</script>
