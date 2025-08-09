import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApiClient } from '../clients/authClient'

export interface User {
  id: number
  username: string
  email: string
  is_active: boolean
  is_admin: boolean
  is_email_verified: boolean
  created_at: string
  last_login?: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
  expires_in: number
}

export interface RegisterResponse {
  message: string
  verification_sent: boolean
}

export interface VerifyEmailResponse {
  message: string
  access_token: string
  token_type: string
  expires_in: number
  user: User
}

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('auth_token'))

  // Configure auth client on startup
  if (token.value) {
    authApiClient.setAuthToken(token.value)
  }

  // Computed
  const isLoggedIn = computed(() => !!token.value && !!user.value)
  const isAdmin = computed(() => user.value?.is_admin || false)
  const isEmailVerified = computed(() => user.value?.is_email_verified || false)
  const userDisplayName = computed(() => user.value?.username || 'Guest')

  // Private helper actions
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

  // Public actions
  const login = async (username: string, password: string) => {
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
    }
  }

  const logout = async () => {
    if (!token.value) return

    try {
      await authApiClient.logout()
    } catch (error) {
      console.error('Logout error:', error)
      // Continue with logout even if server call fails
    } finally {
      clearAuthToken()
    }
  }

  const getCurrentUser = async (): Promise<User | null> => {
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

  const register = async (username: string, email: string, password: string): Promise<RegisterResponse> => {
    try {
      const response = await authApiClient.register(username, email, password)
      return response
    } catch (error) {
      throw error
    }
  }

  const verifyEmail = async (token: string) => {
    try {
      const response = await authApiClient.verifyEmail(token)
      
      if (response.access_token) {
        // User is automatically logged in after verification
        setAuthToken(response.access_token)
        user.value = response.user
        return { success: true, message: response.message }
      }
      
      return { success: false, error: 'No access token received' }
    } catch (error: any) {
      return { success: false, error: error.message || 'Email verification failed' }
    }
  }

  const resendVerificationEmail = async (email: string) => {
    try {
      const response = await authApiClient.resendVerificationEmail(email)
      return response
    } catch (error) {
      throw error
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
    
    // Computed
    isLoggedIn,
    isAdmin,
    isEmailVerified,
    userDisplayName,
    
    // Actions
    login,
    logout,
    register,
    verifyEmail,
    resendVerificationEmail,
    getCurrentUser,
    changePassword,
    verifyToken,
    checkAuthStatus,
    init,
    setAuthToken,
    clearAuthToken
  }
})
