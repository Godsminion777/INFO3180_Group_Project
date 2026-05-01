import { onUnmounted } from 'vue'

export function usePolling(fn, intervalMs = 4000) {
  const timer = setInterval(fn, intervalMs)
  onUnmounted(() => clearInterval(timer))
  return timer
}
