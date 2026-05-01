import api from './index'

export const sendMessage = (receiver_id, content) =>
  api.post('/messages', { receiver_id, content })
export const getConversation = other_user_id =>
  api.get(`/messages/${other_user_id}`)
export const getConversations = () => api.get('/messages/conversations')
