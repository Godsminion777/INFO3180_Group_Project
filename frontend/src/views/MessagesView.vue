<template>
  <div class="min-h-screen bg-linear-to-br from-pink-200 to-blue-200 dark:from-blue-950 dark:to-pink-950">
    <div class="max-w-2xl mx-auto px-4 py-8">
      <h1 class="text-2xl font-bold mb-6 text-gray-900 dark:text-gray-100">Messages</h1>

      <div v-if="loading" class="text-center py-20 text-gray-400">Loading...</div>

      <div v-else-if="messages.conversations.length === 0" class="text-center py-20">
        <div class="text-5xl mb-4">💬</div>
        <p class="text-gray-500">No conversations yet</p>
        <p class="text-sm text-gray-400 mt-1">Match with someone and start chatting!</p>
      </div>

      <div v-else class="space-y-2">
        <router-link
          v-for="convo in messages.conversations"
          :key="convo.user.id"
          :to="`/messages/${convo.user.id}`"
          class="flex items-center gap-4 p-4 bg-white dark:bg-gray-800 rounded-xl shadow-sm hover:shadow-md transition-shadow"
          @click="messages.clearUnread()"
        >
          <div class="w-14 h-14 rounded-full bg-gradient-to-br from-pink-100 to-purple-100 dark:from-pink-900/30 dark:to-purple-900/30 overflow-hidden flex-shrink-0 flex items-center justify-center text-xl">
            <img v-if="convo.profile?.photo_url" :src="convo.profile.photo_url" class="w-full h-full object-cover" />
            <span v-else>👤</span>
          </div>
          <div class="flex-1 min-w-0">
            <div class="flex items-baseline justify-between gap-2">
              <p class="font-semibold text-gray-900 dark:text-gray-100 truncate">
                {{ convo.profile?.first_name || convo.user.username }}
              </p>
              <span v-if="convo.last_message" class="text-xs text-gray-400 flex-shrink-0">
                {{ formatTime(convo.last_message.created_at) }}
              </span>
            </div>
            <p v-if="convo.last_message" class="text-sm text-gray-500 dark:text-gray-400 truncate">
              {{ convo.last_message.content }}
            </p>
            <p v-else class="text-sm text-gray-400 italic">No messages yet</p>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useMessagesStore } from '../stores/messages'

const messages = useMessagesStore()
const loading = ref(false)

function formatTime(dt) {
  if (!dt) return ''
  const d = new Date(dt)
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

onMounted(async () => {
  loading.value = true
  await messages.fetchConversations()
  loading.value = false
})
</script>