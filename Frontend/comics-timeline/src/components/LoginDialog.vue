<template>
  <v-dialog v-model="dialog" max-width="400px" @click:outside="closeDialog">
    <template v-slot:activator="{ props }">
      <v-btn
        v-if="!isLoggedIn"
        variant="outlined"
        color="white"
        prepend-icon="mdi-login"
        v-bind="props"
        class="login-btn"
      >
        Login
      </v-btn>
      <v-menu v-else>
        <template v-slot:activator="{ props }">
          <v-btn
            variant="text"
            color="white"
            prepend-icon="mdi-account-circle"
            v-bind="props"
            class="user-menu-btn"
          >
            {{ userInfo?.username || 'User' }}
          </v-btn>
        </template>
        <v-list>
          <v-list-item @click="logout">
            <v-list-item-title>
              <v-icon>mdi-logout</v-icon>
              Logout
            </v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </template>

    <v-card class="login-dialog">
      <v-card-title class="text-h5 pa-4 bg-primary text-white">
        <v-icon left>mdi-account-circle</v-icon>
        {{ isRegistering ? 'Register for Comics Timeline' : 'Login to Comics Timeline' }}
      </v-card-title>

      <v-card-text class="pa-6">
        <v-form ref="loginForm" v-model="formValid" @submit.prevent="isRegistering ? handleRegister() : handleLogin()">
          <v-text-field
            v-model="loginData.username"
            :rules="usernameRules"
            label="Username"
            prepend-inner-icon="mdi-account"
            variant="outlined"
            class="mb-3"
            :error-messages="fieldErrors.username"
            @input="clearFieldError('username')"
          ></v-text-field>

          <v-text-field
            v-if="isRegistering"
            v-model="loginData.email"
            :rules="emailRules"
            label="Email"
            prepend-inner-icon="mdi-email"
            variant="outlined"
            type="email"
            class="mb-3"
            :error-messages="fieldErrors.email"
            @input="clearFieldError('email')"
          ></v-text-field>

          <v-text-field
            v-model="loginData.password"
            :rules="isRegistering ? registerPasswordRules : passwordRules"
            label="Password"
            prepend-inner-icon="mdi-lock"
            :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
            @click:append-inner="showPassword = !showPassword"
            variant="outlined"
            :type="showPassword ? 'text' : 'password'"
            class="mb-3"
            :error-messages="fieldErrors.password"
            @input="clearFieldError('password')"
          ></v-text-field>

          <v-text-field
            v-if="isRegistering"
            v-model="confirmPassword"
            :rules="confirmPasswordRules"
            label="Confirm Password"
            prepend-inner-icon="mdi-lock-check"
            :append-inner-icon="showConfirmPassword ? 'mdi-eye-off' : 'mdi-eye'"
            @click:append-inner="showConfirmPassword = !showConfirmPassword"
            variant="outlined"
            :type="showConfirmPassword ? 'text' : 'password'"
            class="mb-3"
            :error-messages="fieldErrors.confirmPassword"
            @input="clearFieldError('confirmPassword')"
          ></v-text-field>

          <v-alert
            v-if="errorMessage"
            type="error"
            variant="tonal"
            class="mb-3"
            closable
            @click:close="errorMessage = ''"
          >
            {{ errorMessage }}
          </v-alert>

          <v-alert
            v-if="successMessage"
            type="success"
            variant="tonal"
            class="mb-3"
          >
            {{ successMessage }}
          </v-alert>
        </v-form>
      </v-card-text>

      <v-card-actions class="pa-4 pt-0">
        <v-btn
          variant="text"
          @click="isRegistering ? toggleMode() : closeDialog()"
          :disabled="loading"
        >
          {{ isRegistering ? 'Back to Login' : 'Cancel' }}
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn
          v-if="!isRegistering"
          variant="text"
          @click="toggleMode"
          :disabled="loading"
        >
          Need an account?
        </v-btn>
        <v-btn
          color="primary"
          variant="elevated"
          @click="isRegistering ? handleRegister() : handleLogin()"
          :loading="loading"
          :disabled="loading || (isRegistering ? !isRegistrationValid : !isLoginValid)"
        >
          {{ isRegistering ? 'Register' : 'Login' }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

// Auth store
const authStore = useAuthStore()

// Reactive data
const dialog = ref(false)
const formValid = ref(false)
const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const loginForm = ref()
const isRegistering = ref(false)
const confirmPassword = ref('')
const showPassword = ref(false)
const showConfirmPassword = ref(false)

// Login form data
const loginData = ref({
  username: '',
  email: '',
  password: ''
})

// Field-specific errors
const fieldErrors = ref({
  username: [],
  password: [],
  email: [],
  confirmPassword: []
})

// Form validation rules
const usernameRules = [
  (v: string) => !!v || 'Username is required',
  (v: string) => v.length >= 3 || 'Username must be at least 3 characters',
  (v: string) => v.length <= 50 || 'Username must be less than 50 characters',
  (v: string) => /^[a-zA-Z0-9_-]+$/.test(v) || 'Username can only contain letters, numbers, underscores, and hyphens'
]

const emailRules = [
  (v: string) => !!v || 'Email is required',
  (v: string) => /.+@.+\..+/.test(v) || 'Email must be valid'
]

const passwordRules = [
  (v: string) => !!v || 'Password is required',
  (v: string) => v.length >= 6 || 'Password must be at least 6 characters'
]

const registerPasswordRules = [
  (v: string) => !!v || 'Password is required',
  (v: string) => v.length >= 8 || 'Password must be at least 8 characters',
  (v: string) => v.length <= 100 || 'Password must be less than 100 characters'
]

const confirmPasswordRules = [
  (v: string) => !!v || 'Please confirm your password',
  (v: string) => v === loginData.value.password || 'Passwords do not match'
]

// Computed properties
const isLoggedIn = computed(() => authStore.isLoggedIn)
const userInfo = computed(() => authStore.user)

// Check if registration form is valid
const isRegistrationValid = computed(() => {
  if (!isRegistering.value) return true // Only validate when in registration mode
  
  // Check if all required fields are filled
  const hasUsername = loginData.value.username.trim().length >= 3
  const hasEmail = loginData.value.email.trim().length > 0 && /.+@.+\..+/.test(loginData.value.email)
  const hasPassword = loginData.value.password.length >= 8
  const hasConfirmPassword = confirmPassword.value.length > 0
  const passwordsMatch = loginData.value.password === confirmPassword.value
  
  return hasUsername && hasEmail && hasPassword && hasConfirmPassword && passwordsMatch
})

// Check if login form is valid
const isLoginValid = computed(() => {
  if (isRegistering.value) return true // Only validate when in login mode
  
  const hasUsername = loginData.value.username.trim().length > 0
  const hasPassword = loginData.value.password.length >= 6
  
  return hasUsername && hasPassword
})

// Methods
const clearFieldError = (field: string) => {
  (fieldErrors.value as any)[field] = []
  errorMessage.value = ''
}

const toggleMode = () => {
  isRegistering.value = !isRegistering.value
  
  // Clear form data but keep the mode
  loginData.value = {
    username: '',
    email: '',
    password: ''
  }
  confirmPassword.value = ''
  showPassword.value = false
  showConfirmPassword.value = false
  fieldErrors.value = {
    username: [],
    password: [],
    email: [],
    confirmPassword: []
  }
  errorMessage.value = ''
  successMessage.value = ''
  loading.value = false
}

const closeDialog = () => {
  dialog.value = false
  // Reset everything including the mode when closing
  isRegistering.value = false
  resetForm()
}

const resetForm = () => {
  loginData.value = {
    username: '',
    email: '',
    password: ''
  }
  confirmPassword.value = ''
  showPassword.value = false
  showConfirmPassword.value = false
  fieldErrors.value = {
    username: [],
    password: [],
    email: [],
    confirmPassword: []
  }
  errorMessage.value = ''
  successMessage.value = ''
  loading.value = false
  // Don't reset isRegistering here - let toggleMode handle that
}

const handleLogin = async () => {
  if (!formValid.value) return

  loading.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    await authStore.login(loginData.value.username, loginData.value.password)
    
    successMessage.value = 'Login successful!'
    
    // Close dialog after short delay
    setTimeout(() => {
      closeDialog()
    }, 1000)

  } catch (error: any) {
    console.error('Login error:', error)
    
    if (error.response?.status === 401) {
      errorMessage.value = 'Invalid username or password'
    } else if (error.response?.status === 400) {
      const detail = error.response?.data?.detail || 'Account issue'
      if (detail.includes('verify your email')) {
        errorMessage.value = 'Please verify your email address before logging in. Check your inbox for a verification email.'
      } else {
        errorMessage.value = detail
      }
    } else if (error.response?.data?.detail) {
      errorMessage.value = error.response.data.detail
    } else {
      errorMessage.value = 'Login failed. Please try again.'
    }
  } finally {
    loading.value = false
  }
}

const handleRegister = async () => {
  if (!formValid.value) {
    return
  }

  loading.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    const response = await authStore.register(
      loginData.value.username,
      loginData.value.email,
      loginData.value.password
    )
    
    successMessage.value = response.message || 'Registration successful! Please check your email.'
    
    // Switch back to login mode after successful registration
    setTimeout(() => {
      isRegistering.value = false
      loginData.value.password = ''
      confirmPassword.value = ''
    }, 3000)

  } catch (error: any) {
    console.error('Registration error:', error)
    
    if (error.response?.status === 400) {
      const detail = error.response?.data?.detail || 'Registration failed'
      errorMessage.value = detail
    } else if (error.response?.data?.detail) {
      errorMessage.value = error.response.data.detail
    } else {
      errorMessage.value = 'Registration failed. Please try again.'
    }
  } finally {
    loading.value = false
  }
}

const logout = async () => {
  try {
    await authStore.logout()
  } catch (error) {
    console.error('Logout error:', error)
  }
}

// Initialize auth state on mount
onMounted(() => {
  authStore.checkAuthStatus()
})
</script>

<style scoped>
.login-dialog {
  border-radius: 12px;
}

.login-btn {
  border-color: rgba(255, 255, 255, 0.7);
}

.login-btn:hover {
  border-color: white;
  background-color: rgba(255, 255, 255, 0.1);
}

.user-menu-btn {
  text-transform: none;
}

.user-menu-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
}
</style>
