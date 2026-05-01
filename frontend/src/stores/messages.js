import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as messagesApi from '../api/messages'

export const useMessagesStore = defineStore('messages', () => {
  const conversations = ref([])
  const activeMessages = ref([])
  const activeUserId = ref(null)
  const unreadCount = ref(0)

  async function fetchConversations() {
    const res = await messagesApi.getConversations()
    const prev = conversations.value.length
    conversations.value = res.data.conversations
    if (conversations.value.length > prev) {
      unreadCount.value += conversations.value.length - prev
    }
  }

  async function fetchConversation(userId) {
    activeUserId.value = userId
    const res = await messagesApi.getConversation(userId)
    activeMessages.value = res.data.messages
  }

  async function send(receiverId, content) {
    const res = await messagesApi.sendMessage(receiverId, content)
    activeMessages.value.push(res.data.data)
    return res.data
  }

  async function poll(userId) {
    if (!userId) return
    const res = await messagesApi.getConversation(userId)
    activeMessages.value = res.data.messages
  }

  function clearUnread() {
    unreadCount.value = 0
  }

  return { conversations, activeMessages, activeUserId, unreadCount, fetchConversations, fetchConversation, send, poll, clearUnread }
})
