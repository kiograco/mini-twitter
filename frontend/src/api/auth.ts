import apiClient from './client'

export const authService = {
  async login(email: string, password: string) {
    const response = await apiClient.post<{ token: string; user: any }>('/auth/login', { email, password })
    return {
      token: response.data.token,
      user: response.data.user,
    }
  },

  async register(username: string, email: string, password: string) {
    await apiClient.post('/auth/register', { username, email, password })
  },

  async refreshToken() {
    const response = await apiClient.post<{ token: string }>('/auth/refresh')
    return response.data.token
  },

  async logout() {
    await apiClient.post('/auth/logout')
  },
}