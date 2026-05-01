<template>
  <div class="fixed bottom-4 right-4 flex flex-col gap-2 z-50">
    <transition-group name="toast">
      <div
        v-for="n in ui.notifications"
        :key="n.id"
        class="flex items-center gap-3 px-4 py-3 rounded-lg shadow-lg text-white text-sm max-w-xs cursor-pointer"
        :class="typeClass(n.type)"
        @click="ui.dismiss(n.id)"
      >
        <span>{{ typeIcon(n.type) }}</span>
        <span>{{ n.message }}</span>
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { useUiStore } from '../stores/ui'

const ui = useUiStore()

function typeClass(type) {
  return {
    success: 'bg-green-500',
    error: 'bg-red-500',
    warning: 'bg-yellow-500',
    info: 'bg-blue-500',
    match: 'bg-pink-500'
  }[type] || 'bg-gray-700'
}

function typeIcon(type) {
  return { success: '✅', error: '❌', warning: '⚠️', info: 'ℹ️', match: '💕' }[type] || '🔔'
}
</script>

<style scoped>
@reference "tailwindcss";
.toast-enter-active, .toast-leave-active { transition: all 0.3s ease; }
.toast-enter-from { transform: translateX(100%); opacity: 0; }
.toast-leave-to { transform: translateX(100%); opacity: 0; }
</style>
