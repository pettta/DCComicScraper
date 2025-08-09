// Export all stores from a central location
export { useAuthStore } from './auth'
export { useUIStore } from './ui'

// Export store types for convenience
export type { User, LoginResponse, RegisterResponse, VerifyEmailResponse } from './auth'
export type { NotificationState, DialogState } from './ui'
