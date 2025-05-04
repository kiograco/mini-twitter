import apiClient from './client'

export const postService = {
  async getFeed() {
    const response = await apiClient.get('/posts/')
    return response.data
  },
  async createPost(content: string) {
    const response = await apiClient.post('/posts/create', { content })
    return response.data
  },
  async likePost(postId: string) {
    const response = await apiClient.post(`/posts/${postId}/like`)
    return response.data
  },
  async unlikePost(postId: string) {
    const response = await apiClient.post(`/posts/${postId}/unlike`)
    return response.data
  },
  async getPost(postId: string) {
    const response = await apiClient.get(`/posts/${postId}`)
    return response.data
  },
  async deletePost(postId: string) {
    const response = await apiClient.delete(`/posts/${postId}`)
    return response.data
  },
  async updatePost(postId: string, data: { content: string }) {
    const response = await apiClient.patch(`/posts/${postId}`, data)
    return response.data
  },
}