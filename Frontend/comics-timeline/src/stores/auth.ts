import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApiClient } from '../clients/authClient'

interface User {
  id: number
  username: string
  email: string
  is_active: boolean
  is_admin: boolean
  created_at: string
  last_login?: string
}

interface LoginResponse {
  access_token: string
  token_type: string
  expires_in: number
}

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('auth_token'))
  const isLoading = ref(false)

  // Configure auth client on startup
  if (token.value) {
    authApiClient.setAuthToken(token.value)
  }

  // Computed
  const isLoggedIn = computed(() => !!token.value && !!user.value)
  const isAdmin = computed(() => user.value?.is_admin || false)

  // Actions
  const setAuthToken = (newToken: string) => {
    token.value = newToken
    localStorage.setItem('auth_token', newToken)
    authApiClient.setAuthToken(newToken)
  }

  const clearAuthToken = () => {
    token.value = null
    user.value = null
    localStorage.removeItem('auth_token')
    authApiClient.clearAuthToken()
  }

  const login = async (username: string, password: string) => {
    isLoading.value = true
    
    try {
      const response = await authApiClient.login(username, password)
      const { access_token } = response
      setAuthToken(access_token)

      // Get user info
      await getCurrentUser()

      return response
    } catch (error) {
      clearAuthToken()
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const logout = async () => {
    if (!token.value) return

    try {
      await authApiClient.logout()
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      clearAuthToken()
    }
  }

  const getCurrentUser = async () => {
    if (!token.value) return null

    try {
      const response = await authApiClient.getCurrentUser()
      user.value = response
      return response
    } catch (error) {
      console.error('Get current user error:', error)
      clearAuthToken()
      throw error
    }
  }

  const register = async (username: string, email: string, password: string) => {
    isLoading.value = true

    try {
      const response = await authApiClient.register(username, email, password)
      return response
    } catch (error) {
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const changePassword = async (currentPassword: string, newPassword: string) => {
    try {
      const response = await authApiClient.changePassword(currentPassword, newPassword)
      return response
    } catch (error) {
      throw error
    }
  }

  const verifyToken = async () => {
    if (!token.value) return false

    try {
      const response = await authApiClient.verifyToken()
      return response.valid
    } catch (error) {
      console.error('Token verification error:', error)
      clearAuthToken()
      return false
    }
  }

  const checkAuthStatus = async () => {
    if (!token.value) return

    try {
      const isValid = await verifyToken()
      if (isValid && !user.value) {
        await getCurrentUser()
      }
    } catch (error) {
      console.error('Auth status check error:', error)
      clearAuthToken()
    }
  }

  // Initialize store
  const init = () => {
    if (token.value) {
      checkAuthStatus()
    }
  }

  return {
    // State
    user,
    token,
    isLoading,
    
    // Computed
    isLoggedIn,
    isAdmin,
    
    // Actions
    login,
    logout,
    register,
    getCurrentUser,
    changePassword,
    verifyToken,
    checkAuthStatus,
    init,
    setAuthToken,
    clearAuthToken
  }
})
