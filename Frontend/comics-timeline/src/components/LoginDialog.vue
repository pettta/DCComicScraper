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
        Login to Comics Timeline
      </v-card-title>

      <v-card-text class="pa-6">
        <v-form ref="loginForm" v-model="formValid" @submit.prevent="handleLogin">
          <v-text-field
            v-model="loginData.username"
            :rules="usernameRules"
            label="Username or Email"
            prepend-inner-icon="mdi-account"
            variant="outlined"
            class="mb-3"
            :error-messages="fieldErrors.username"
            @input="clearFieldError('username')"
          ></v-text-field>

          <v-text-field
            v-model="loginData.password"
            :rules="passwordRules"
            label="Password"
            prepend-inner-icon="mdi-lock"
            variant="outlined"
            type="password"
            class="mb-3"
            :error-messages="fieldErrors.password"
            @input="clearFieldError('password')"
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
          @click="closeDialog"
          :disabled="loading"
        >
          Cancel
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          variant="elevated"
          @click="handleLogin"
          :loading="loading"
          :disabled="!formValid || loading"
        >
          Login
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'

// Auth store
const authStore = useAuthStore()

// Reactive data
const dialog = ref(false)
const formValid = ref(false)
const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const loginForm = ref()

// Login form data
const loginData = ref({
  username: '',
  password: ''
})

// Field-specific errors
const fieldErrors = ref({
  username: [],
  password: []
})

// Form validation rules
const usernameRules = [
  (v: string) => !!v || 'Username or email is required',
  (v: string) => v.length >= 3 || 'Username must be at least 3 characters'
]

const passwordRules = [
  (v: string) => !!v || 'Password is required',
  (v: string) => v.length >= 6 || 'Password must be at least 6 characters'
]

// Computed properties
const isLoggedIn = computed(() => authStore.isLoggedIn)
const userInfo = computed(() => authStore.user)

// Methods
const clearFieldError = (field: string) => {
  fieldErrors.value[field] = []
  errorMessage.value = ''
}

const closeDialog = () => {
  dialog.value = false
  resetForm()
}

const resetForm = () => {
  loginData.value = {
    username: '',
    password: ''
  }
  fieldErrors.value = {
    username: [],
    password: []
  }
  errorMessage.value = ''
  successMessage.value = ''
  loading.value = false
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
      errorMessage.value = 'Account is inactive'
    } else if (error.response?.data?.detail) {
      errorMessage.value = error.response.data.detail
    } else {
      errorMessage.value = 'Login failed. Please try again.'
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
