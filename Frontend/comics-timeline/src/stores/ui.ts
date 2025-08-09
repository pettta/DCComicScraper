import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface NotificationState {
  show: boolean
  message: string
  type: 'success' | 'error' | 'warning' | 'info'
  timeout?: number
}

export interface DialogState {
  show: boolean
  title?: string
  message?: string
  persistent?: boolean
}

export const useUIStore = defineStore('ui', () => {
  // Loading states
  const globalLoading = ref(false)
  const pageLoading = ref(false)
  const componentLoadingStates = ref<Record<string, boolean>>({})

  // Dialog states
  const loginDialog = ref(false)
  const confirmDialog = ref<DialogState>({
    show: false,
    title: '',
    message: '',
    persistent: false
  })

  // Notification/Snackbar state
  const notification = ref<NotificationState>({
    show: false,
    message: '',
    type: 'info',
    timeout: 4000
  })

  // Sidebar/Navigation state
  const sidebarOpen = ref(false)
  const navigationDrawer = ref(false)

  // Theme and layout
  const darkTheme = ref(localStorage.getItem('theme') === 'dark')
  const fullscreenMode = ref(false)

  // Form states
  const formErrors = ref<Record<string, string[]>>({})
  const formLoading = ref<Record<string, boolean>>({})

  // Actions for loading states
  const setGlobalLoading = (loading: boolean) => {
    globalLoading.value = loading
  }

  const setPageLoading = (loading: boolean) => {
    pageLoading.value = loading
  }

  const setComponentLoading = (componentKey: string, loading: boolean) => {
    componentLoadingStates.value[componentKey] = loading
  }

  const clearComponentLoading = (componentKey: string) => {
    delete componentLoadingStates.value[componentKey]
  }

  // Actions for dialogs
  const openLoginDialog = () => {
    loginDialog.value = true
  }

  const closeLoginDialog = () => {
    loginDialog.value = false
  }

  const openConfirmDialog = (title: string, message: string, persistent = false) => {
    confirmDialog.value = {
      show: true,
      title,
      message,
      persistent
    }
  }

  const closeConfirmDialog = () => {
    confirmDialog.value.show = false
  }

  // Actions for notifications
  const showNotification = (
    message: string, 
    type: NotificationState['type'] = 'info', 
    timeout = 4000
  ) => {
    notification.value = {
      show: true,
      message,
      type,
      timeout
    }
  }

  const showSuccess = (message: string, timeout = 4000) => {
    showNotification(message, 'success', timeout)
  }

  const showError = (message: string, timeout = 6000) => {
    showNotification(message, 'error', timeout)
  }

  const showWarning = (message: string, timeout = 5000) => {
    showNotification(message, 'warning', timeout)
  }

  const showInfo = (message: string, timeout = 4000) => {
    showNotification(message, 'info', timeout)
  }

  const hideNotification = () => {
    notification.value.show = false
  }

  // Actions for navigation
  const toggleSidebar = () => {
    sidebarOpen.value = !sidebarOpen.value
  }

  const openSidebar = () => {
    sidebarOpen.value = true
  }

  const closeSidebar = () => {
    sidebarOpen.value = false
  }

  const toggleNavigationDrawer = () => {
    navigationDrawer.value = !navigationDrawer.value
  }

  // Actions for theme
  const toggleTheme = () => {
    darkTheme.value = !darkTheme.value
    localStorage.setItem('theme', darkTheme.value ? 'dark' : 'light')
  }

  const setTheme = (dark: boolean) => {
    darkTheme.value = dark
    localStorage.setItem('theme', dark ? 'dark' : 'light')
  }

  const toggleFullscreen = () => {
    fullscreenMode.value = !fullscreenMode.value
  }

  // Actions for forms
  const setFormLoading = (formKey: string, loading: boolean) => {
    formLoading.value[formKey] = loading
  }

  const clearFormLoading = (formKey: string) => {
    delete formLoading.value[formKey]
  }

  const setFormErrors = (formKey: string, errors: string[]) => {
    formErrors.value[formKey] = errors
  }

  const clearFormErrors = (formKey: string) => {
    delete formErrors.value[formKey]
  }

  const clearAllFormErrors = () => {
    formErrors.value = {}
  }

  // Utility actions
  const resetUIState = () => {
    // Reset all UI state to defaults (useful for logout, etc.)
    globalLoading.value = false
    pageLoading.value = false
    componentLoadingStates.value = {}
    loginDialog.value = false
    confirmDialog.value = { show: false, title: '', message: '', persistent: false }
    notification.value = { show: false, message: '', type: 'info', timeout: 4000 }
    sidebarOpen.value = false
    navigationDrawer.value = false
    fullscreenMode.value = false
    formErrors.value = {}
    formLoading.value = {}
  }

  return {
    // State
    globalLoading,
    pageLoading,
    componentLoadingStates,
    loginDialog,
    confirmDialog,
    notification,
    sidebarOpen,
    navigationDrawer,
    darkTheme,
    fullscreenMode,
    formErrors,
    formLoading,

    // Loading actions
    setGlobalLoading,
    setPageLoading,
    setComponentLoading,
    clearComponentLoading,

    // Dialog actions
    openLoginDialog,
    closeLoginDialog,
    openConfirmDialog,
    closeConfirmDialog,

    // Notification actions
    showNotification,
    showSuccess,
    showError,
    showWarning,
    showInfo,
    hideNotification,

    // Navigation actions
    toggleSidebar,
    openSidebar,
    closeSidebar,
    toggleNavigationDrawer,

    // Theme actions
    toggleTheme,
    setTheme,
    toggleFullscreen,

    // Form actions
    setFormLoading,
    clearFormLoading,
    setFormErrors,
    clearFormErrors,
    clearAllFormErrors,

    // Utility actions
    resetUIState
  }
})
