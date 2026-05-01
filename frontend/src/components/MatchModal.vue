<template>
  <transition name="modal">
    <div v-if="show" class="fixed inset-0 bg-black/60 flex items-center justify-center z-50" @click.self="$emit('close')">
      <div class="bg-white dark:bg-gray-800 rounded-2xl p-8 text-center max-w-sm w-full mx-4 shadow-2xl">
        <div class="text-6xl mb-4">💕</div>
        <h2 class="text-2xl font-bold text-pink-500 mb-2">It's a Match!</h2>
        <p class="text-gray-600 dark:text-gray-300 mb-6">You and {{ matchName }} liked each other!</p>
        <div class="flex gap-3">
          <button @click="$emit('message')" class="flex-1 py-2 bg-pink-500 text-white rounded-full font-medium hover:bg-pink-600">
            Send Message
          </button>
          <button @click="$emit('close')" class="flex-1 py-2 border border-gray-300 dark:border-gray-600 rounded-full hover:bg-gray-50 dark:hover:bg-gray-700">
            Keep Browsing
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
defineProps({ show: Boolean, matchName: String })
defineEmits(['close', 'message'])
</script>

<style scoped>
@reference "tailwindcss";
.modal-enter-active, .modal-leave-active { transition: opacity 0.3s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
</style>
