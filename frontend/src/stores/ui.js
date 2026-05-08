import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useUiStore = defineStore('ui', () => {
  //const darkMode = ref(localStorage.getItem('darkMode') === 'true')
  const stored = localStorage.getItem('darkMode')
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
  const darkMode = ref(stored !== null ? stored === 'true' : prefersDark)
  
  const notifications = ref([])
  let nextId = 0

  watch(darkMode, val => {
    localStorage.setItem('darkMode', val)
    document.documentElement.classList.toggle('dark', val)
  }, { immediate: true })

  function toggleDark() {
    darkMode.value = !darkMode.value
  }

  function notify(message, type = 'info', duration = 4000) {
    const id = ++nextId
    notifications.value.push({ id, message, type })
    setTimeout(() => dismiss(id), duration)
  }

  function dismiss(id) {
    notifications.value = notifications.value.filter(n => n.id !== id)
  }

  return { darkMode, notifications, toggleDark, notify, dismiss }
})
