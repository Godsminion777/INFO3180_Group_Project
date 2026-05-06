import api from './index'

export const register = data => api.post('backend/app/views/auth/register', data)
export const login = data => api.post('backend/app/views/auth/login', data)
export const logout = () => api.post('backend/app/views/auth/logout', { action: 'logout' })
export const getMe = () => api.get('backend/app/views/auth/me')