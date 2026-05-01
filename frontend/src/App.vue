<template>
  <div :class="{ dark: ui.darkMode }">
    <Navbar />
    <main>
      <RouterView />
    </main>
    <NotificationToast />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import Navbar from './components/Navbar.vue'
import NotificationToast from './components/NotificationToast.vue'
import { useUiStore } from './stores/ui'
import { useMessagesStore } from './stores/messages'
import { useAuthStore } from './stores/auth'
import { usePolling } from './composables/usePolling'

const ui = useUiStore()
const auth = useAuthStore()
const messages = useMessagesStore()

usePolling(async () => {
  if (auth.isLoggedIn) {
    await messages.fetchConversations()
  }
}, 8000)
</script>
