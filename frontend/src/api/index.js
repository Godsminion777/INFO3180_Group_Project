import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  withCredentials: true,
  headers: { 'Content-Type': 'application/json' }
})

// Sends user back to login if is invalid
api.interceptors.response.use(
  res => res,
  err => {
    if (err.response?.status === 401) {
      // Don't redirect on the auth-check call itself
      const isAuthCheck = err.config?.url?.endsWith('/auth/me')
      // Don't redirect if already on login/register
      const onPublicPage = ['/login', '/register'].some(p => window.location.pathname.startsWith(p)
      )
      
      if (!isAuthCheck && !onPublicPage) {
        window.location.href = '/login'
      }
    }
    return Promise.reject(err)
  }
)

export default api
