<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-shadow">
    <div class="relative h-48 bg-linear-to-br from-pink-100 to-purple-100 dark:from-pink-900/30 dark:to-purple-900/30">
      <img
        v-if="profile.photo_url"
        :src="`http://127.0.0.1:5000/${profile.photo_url}`"
        :alt="`${profile.first_name}'s photo`"
        class="w-full h-full object-cover"
      />
      <div v-else class="w-full h-full flex items-center justify-center text-5xl">👤</div>
      <button
        @click.prevent="$emit('save', profile.id)"
        class="absolute top-2 right-2 p-2 bg-white/80 dark:bg-gray-800/80 rounded-full text-lg hover:scale-110 transition-transform"
      >
        {{ isSaved ? '❤️' : '🤍' }}
      </button>
    </div>
    <div class="p-4">
      <div class="flex items-baseline gap-2 mb-1">
        <h3 class="font-semibold text-gray-900 dark:text-gray-100">{{ profile.first_name }} {{ profile.last_name }}</h3>
        <span class="text-gray-500 dark:text-gray-400 text-sm">{{ profile.age }}</span>
      </div>
      <p v-if="profile.location" class="text-xs text-gray-500 dark:text-gray-400 mb-2">📍 {{ profile.location }}</p>
      <p v-if="profile.bio" class="text-sm text-gray-600 dark:text-gray-300 line-clamp-2 mb-3">{{ profile.bio }}</p>
      <div v-if="profile.interests?.length" class="flex flex-wrap gap-1">
        <span
          v-for="interest in profile.interests.slice(0, 4)"
          :key="interest"
          class="text-xs px-2 py-0.5 bg-pink-50 dark:bg-pink-900/30 text-pink-600 dark:text-pink-300 rounded-full"
        >
          {{ interest }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  profile: { type: Object, required: true },
  isSaved: { type: Boolean, default: false }
})
defineEmits(['save'])
</script>
