import api from './index'

export const doAction = (receiver_id, action) =>
  api.post('/matches/action', { receiver_id, action })
export const getMutualMatches = () => api.get('/matches')
export const getPotentialMatches = () => api.get('/matches/potential')
