import api from './index'

export const getAllProfiles = () => api.get('/profiles')
export const getProfile = id => api.get(`/profiles/${id}`)
export const updateProfile = (id, data) => api.put(`/profiles/${id}`, data)
export const uploadPhoto = (id, formData) =>
  api.post(`/profiles/${id}/photo`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
