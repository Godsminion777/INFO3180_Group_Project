<template>
  <nav class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700 sticky top-0 z-40">
    <div class="max-w-5xl mx-auto px-4 flex items-center justify-between h-14">
      <router-link to="/browse" class="text-xl font-bold text-blue-500">🌊 DriftDater</router-link>

      <div v-if="auth.isLoggedIn" class="flex items-center gap-4">
        <router-link to="/browse" class="nav-link">Browse</router-link>
        <router-link to="/matches" class="nav-link">Matches</router-link>
        <router-link to="/messages" class="nav-link relative">
          Messages
          <span v-if="msgStore.unreadCount" class="absolute -top-1 -right-2 bg-pink-500 text-white text-xs rounded-full w-4 h-4 flex items-center justify-center">
            {{ msgStore.unreadCount }}
          </span>
        </router-link>
        <router-link to="/search" class="nav-link">Search</router-link>
        <router-link to="/saved" class="nav-link">Saved</router-link>
        <router-link :to="`/profile/${auth.user?.id}`" class="nav-link">Profile</router-link>

        <button @click="ui.toggleDark()" class="p-1 rounded hover:bg-gray-100 dark:hover:bg-gray-700 text-lg">
          {{ ui.darkMode ? '☀️' : '🌙' }}
        </button>

        <button @click="handleLogout" class="px-3 py-1 text-sm bg-gray-100 dark:bg-gray-700 rounded hover:bg-gray-200 dark:hover:bg-gray-600">
          Logout
        </button>
      </div>

      <div v-else class="flex gap-3">
        <router-link to="/login" class="nav-link">Login</router-link>
        <router-link to="/register" class="px-4 py-1 bg-blue-500 text-white rounded-full text-sm hover:bg-pink-700">Sign up</router-link>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useAuthStore } from '../stores/auth'
import { useMessagesStore } from '../stores/messages'
import { useUiStore } from '../stores/ui'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const msgStore = useMessagesStore()
const ui = useUiStore()
const router = useRouter()

async function handleLogout() {
  await auth.logout()
  router.push('/login')
}
</script>

<style scoped>
@reference "tailwindcss";
.nav-link {
  @apply text-sm text-gray-600 dark:text-gray-300 hover:text-pink-500 dark:hover:text-pink-400 relative transition-colors;
}
</style>
