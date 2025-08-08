<template>
  <v-container class="fill-height">
    <v-row justify="center" align="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="mx-auto pa-6" elevation="8">
          <v-card-title class="text-center mb-4">
            <v-icon size="48" color="primary" class="mb-4">mdi-email-check</v-icon>
            <div class="text-h5">Email Verification</div>
          </v-card-title>

          <!-- Loading state -->
          <div v-if="isVerifying" class="text-center py-8">
            <v-progress-circular
              indeterminate
              size="64"
              color="primary"
              class="mb-4"
            ></v-progress-circular>
            <div class="text-h6 mb-2">Verifying your email...</div>
            <div class="text-body-2 text-medium-emphasis">
              Please wait while we verify your account
            </div>
          </div>

          <!-- Success state -->
          <div v-else-if="verificationSuccess" class="text-center py-8">
            <v-icon size="64" color="success" class="mb-4">mdi-check-circle</v-icon>
            <div class="text-h6 mb-2 text-success">Email Verified Successfully!</div>
            <div class="text-body-2 text-medium-emphasis mb-4">
              Your account has been activated and you are now logged in.
            </div>
            <v-btn
              color="primary"
              variant="elevated"
              size="large"
              @click="goToTimeline"
              prepend-icon="mdi-timeline"
            >
              Go to Timeline
            </v-btn>
          </div>

          <!-- Error state -->
          <div v-else-if="verificationError" class="text-center py-8">
            <v-icon size="64" color="error" class="mb-4">mdi-alert-circle</v-icon>
            <div class="text-h6 mb-2 text-error">Verification Failed</div>
            <div class="text-body-2 text-medium-emphasis mb-4">
              {{ errorMessage }}
            </div>
            
            <div class="d-flex flex-column ga-2">
              <v-btn
                color="primary"
                variant="outlined"
                @click="resendVerification"
                :loading="isResending"
                prepend-icon="mdi-email-send"
              >
                Resend Verification Email
              </v-btn>
              
              <v-btn
                color="secondary"
                variant="text"
                @click="goToLogin"
                prepend-icon="mdi-login"
              >
                Back to Login
              </v-btn>
            </div>
          </div>

          <!-- No token provided -->
          <div v-else class="text-center py-8">
            <v-icon size="64" color="warning" class="mb-4">mdi-email-alert</v-icon>
            <div class="text-h6 mb-2 text-warning">Invalid Verification Link</div>
            <div class="text-body-2 text-medium-emphasis mb-4">
              The verification link appears to be invalid or missing.
            </div>
            <v-btn
              color="secondary"
              variant="outlined"
              @click="goToLogin"
              prepend-icon="mdi-login"
            >
              Back to Login
            </v-btn>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <!-- Success snackbar -->
    <v-snackbar
      v-model="showSuccessSnackbar"
      color="success"
      timeout="3000"
      location="top"
    >
      <v-icon>mdi-check-circle</v-icon>
      {{ successMessage }}
    </v-snackbar>

    <!-- Error snackbar -->
    <v-snackbar
      v-model="showErrorSnackbar"
      color="error"
      timeout="5000"
      location="top"
    >
      <v-icon>mdi-alert-circle</v-icon>
      {{ errorMessage }}
    </v-snackbar>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

// State
const isVerifying = ref(false)
const verificationSuccess = ref(false)
const verificationError = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const showSuccessSnackbar = ref(false)
const showErrorSnackbar = ref(false)
const isResending = ref(false)

// Get token from URL
const token = route.query.token as string

const verifyEmail = async () => {
  if (!token) {
    verificationError.value = true
    errorMessage.value = 'No verification token provided'
    return
  }

  isVerifying.value = true
  verificationError.value = false

  try {
    const response = await authStore.verifyEmail(token)
    
    if (response.success) {
      verificationSuccess.value = true
      successMessage.value = 'Email verified successfully! You are now logged in.'
      showSuccessSnackbar.value = true
      
      // User is automatically logged in after verification
      // The auth store should be updated by the verifyEmail method
    } else {
      throw new Error(response.error || 'Verification failed')
    }
  } catch (error: any) {
    verificationError.value = true
    errorMessage.value = error.message || 'Failed to verify email. The link may be expired or invalid.'
    showErrorSnackbar.value = true
  } finally {
    isVerifying.value = false
  }
}

const resendVerification = async () => {
  isResending.value = true
  
  try {
    // We don't have the email from the token, so we'll need to ask the user
    // For now, show a message directing them to the login page
    successMessage.value = 'Please go to the login page to resend verification email'
    showSuccessSnackbar.value = true
    
    setTimeout(() => {
      goToLogin()
    }, 2000)
  } catch (error: any) {
    errorMessage.value = 'Failed to resend verification email'
    showErrorSnackbar.value = true
  } finally {
    isResending.value = false
  }
}

const goToTimeline = () => {
  router.push('/timeline')
}

const goToLogin = () => {
  router.push('/')
}

onMounted(() => {
  verifyEmail()
})
</script>

<style scoped>
.v-card {
  border-radius: 12px;
}

.v-progress-circular {
  margin: 0 auto;
}
</style>
