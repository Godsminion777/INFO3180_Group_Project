<template>
  <div class="max-w-2xl mx-auto px-4 py-4 flex flex-col h-[calc(100vh-56px)]">
    <!-- Header -->
    <div class="flex items-center gap-3 mb-4 pb-4 border-b border-gray-200 dark:border-gray-700">
      <router-link to="/messages" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200">← Back</router-link>
      <div class="w-10 h-10 rounded-full bg-gradient-to-br from-pink-100 to-purple-100 dark:from-pink-900/30 dark:to-purple-900/30 overflow-hidden flex items-center justify-center text-lg">
        <img v-if="otherProfile?.photo_url" :src="otherProfile.photo_url" class="w-full h-full object-cover" />
        <span v-else>👤</span>
      </div>
      <div>
        <p class="font-semibold text-gray-900 dark:text-gray-100">{{ otherProfile?.first_name || 'Chat' }}</p>
        <p class="text-xs text-green-500">Online</p>
      </div>
      <router-link v-if="otherProfile" :to="`/profile/${otherProfile.id}`" class="ml-auto text-sm text-pink-500 hover:underline">View Profile</router-link>
    </div>

    <!-- Messages -->
    <div class="flex-1 overflow-y-auto space-y-3 mb-4" ref="scrollContainer">
      <div v-if="loading" class="text-center text-gray-400 py-4">Loading messages...</div>

      <div
        v-for="msg in messages.activeMessages"
        :key="msg.id"
        :class="msg.sender_id === auth.user?.id ? 'flex justify-end' : 'flex justify-start'"
      >
        <div
          :class="[
            'max-w-[70%] px-4 py-2 rounded-2xl text-sm',
            msg.sender_id === auth.user?.id
              ? 'bg-pink-500 text-white rounded-br-sm'
              : 'bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-bl-sm shadow-sm'
          ]"
        >
          <p>{{ msg.content }}</p>
          <p class="text-xs mt-1 opacity-60">{{ formatTime(msg.created_at) }}</p>
        </div>
      </div>

      <div v-if="messages.activeMessages.length === 0 && !loading" class="text-center py-8 text-gray-400 text-sm">
        Say hello! 👋
      </div>
    </div>

    <!-- Input -->
    <form @submit.prevent="sendMsg" class="flex gap-2">
      <input
        v-model="newMessage"
        type="text"
        placeholder="Type a message..."
        class="flex-1 px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-full bg-white dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-pink-300 text-sm"
        @keydown.enter.prevent="sendMsg"
      />
      <button
        type="submit"
        :disabled="!newMessage.trim() || sending"
        class="w-10 h-10 bg-pink-500 text-white rounded-full flex items-center justify-center hover:bg-pink-600 disabled:opacity-50 transition-colors"
      >
        →
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useMessagesStore } from '../stores/messages'
import { useProfilesStore } from '../stores/profiles'
import { useUiStore } from '../stores/ui'
import { usePolling } from '../composables/usePolling'

const route = useRoute()
const auth = useAuthStore()
const messages = useMessagesStore()
const profilesStore = useProfilesStore()
const ui = useUiStore()

const loading = ref(false)
const sending = ref(false)
const newMessage = ref('')
const scrollContainer = ref(null)
const otherProfile = ref(null)

function scrollToBottom() {
  nextTick(() => {
    if (scrollContainer.value) {
      scrollContainer.value.scrollTop = scrollContainer.value.scrollHeight
    }
  })
}

function formatTime(dt) {
  if (!dt) return ''
  return new Date(dt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

async function sendMsg() {
  if (!newMessage.value.trim()) return
  sending.value = true
  try {
    await messages.send(Number(route.params.userId), newMessage.value.trim())
    newMessage.value = ''
    scrollToBottom()
  } catch (e) {
    ui.notify(e.response?.data?.error || 'Failed to send', 'error')
  }
  sending.value = false
}

watch(() => messages.activeMessages.length, scrollToBottom)

usePolling(() => messages.poll(Number(route.params.userId)), 4000)

onMounted(async () => {
  loading.value = true
  await messages.fetchConversation(Number(route.params.userId))
  try {
    otherProfile.value = await profilesStore.fetchOneByUserId(route.params.userId)
  } catch {}
  loading.value = false
  scrollToBottom()
})
</script>
