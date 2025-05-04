import apiClient from './client'

export const userService = {
    async getMe() {
        const response = await apiClient.get('/users/me')
        return response.data
    },

    async updateProfile(data: { username?: string; avatar?: string }) {
        const response = await apiClient.patch('/users/me', data)
        return response.data
    },
}