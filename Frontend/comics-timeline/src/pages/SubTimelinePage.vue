<template>
  <div class="sub-timeline-page">
    <!-- Background Elements -->
    <div class="background-container">
      <div class="gradient-bg"></div>
      <div class="grid-pattern"></div>
      <div class="floating-shapes">
        <div class="shape shape-1"></div>
        <div class="shape shape-2"></div>
        <div class="shape shape-3"></div>
      </div>
    </div>

    <!-- Header -->
    <v-app-bar color="#2c3e50" dark elevation="0" height="120" class="header-glass">
      <v-container class="d-flex justify-space-between align-center">
        
        <!-- The Order Nexus Button (Top Left) -->
        <div class="d-flex align-center">
          <v-btn
            variant="text"
            color="white"
            class="text-h5 font-weight-bold mr-4"
            @click="goToHome"
            style="text-transform: none;"
          >
            The Order Nexus
          </v-btn>
          <v-btn
            icon="mdi-arrow-left"
            variant="text"
            @click="goBack"
            class="mr-3"
          ></v-btn>
          <div>
            <h2 class="text-h5">Selected Timeline Sections</h2>
            <p class="text-body-2 mb-0">{{ selectedEras.length }} section(s) loaded</p>
          </div>
        </div>
        
        <div class="text-center flex-grow-1">
          <h1 class="text-h3 mb-2 header-title">{{ publisher }} Comics Timeline</h1>
          <p class="text-h6 mb-0 header-subtitle">Filtered View</p>
        </div>
        
        <div class="d-flex align-center ga-4">
          <div class="publisher-info">
            <v-chip color="primary" variant="elevated" size="large">
              {{ publisher }}
            </v-chip>
          </div>
          
          <!-- Login Dialog -->
          <LoginDialog />
        </div>
      </v-container>
    </v-app-bar>

    <!-- Main Content -->
    <v-main class="main-content">
      <v-container fluid class="pa-8 content-container">
        <v-row>
          <v-col cols="12">
            <!-- Selected Sections Info -->
            <v-card class="mb-4 pa-4" elevation="4">
              <v-card-title class="text-h6 pb-2">
                Active Timeline Sections
              </v-card-title>
              <v-card-text>
                <div class="d-flex flex-wrap gap-2 mb-3">
                  <v-chip
                    v-for="era in selectedEras"
                    :key="era"
                    color="primary"
                    variant="elevated"
                    closable
                    @click:close="removeSection(era)"
                  >
                    {{ era }}
                  </v-chip>
                </div>
                <v-alert
                  v-if="selectedEras.length > 1"
                  type="warning"
                  variant="tonal"
                  density="compact"
                >
                  Multiple sections selected - Some filters may be disabled
                </v-alert>
              </v-card-text>
            </v-card>
            
            <!-- Empty Timeline Placeholder -->
            <div class="timeline-wrapper">
              <v-card class="pa-8 text-center timeline-placeholder" elevation="8">
                <v-icon icon="mdi-timeline-outline" size="80" color="primary" class="mb-4"></v-icon>
                <h3 class="text-h5 mb-3">Filtered Timeline View</h3>
                <p class="text-body-1 mb-4 text-medium-emphasis">
                  This is where the filtered timeline for your selected sections will appear.
                </p>
                <p class="text-body-2 text-medium-emphasis">
                  Selected sections: {{ selectedEras.join(', ') || 'None' }}
                </p>
                
                <!-- Future implementation placeholder -->
                <v-divider class="my-4"></v-divider>
                <p class="text-caption text-disabled">
                  Timeline filtering and detailed view coming soon...
                </p>
              </v-card>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import LoginDialog from '../components/LoginDialog.vue'

// Import modular styles
import '../styles/index.css'

// Props
const props = defineProps<{
  selectedEras?: string[]
}>()

// Router
const router = useRouter()
const route = useRoute()

// Reactive data
const selectedEras = ref<string[]>(props.selectedEras || [])
const publisher = ref<string>('DC')

// Get data from URL params
onMounted(() => {
  // Get selected eras from route query
  if (route.query.sections) {
    const sections = Array.isArray(route.query.sections) 
      ? route.query.sections 
      : [route.query.sections]
    selectedEras.value = sections as string[]
  }
  
  // Get publisher from route query
  if (route.query.publisher && typeof route.query.publisher === 'string') {
    publisher.value = route.query.publisher
  }
  
  console.log('SubTimelinePage initialized with:', {
    selectedEras: selectedEras.value,
    publisher: publisher.value
  })
})

// Navigation methods
const goBack = () => {
  router.push('/')
}

const goToHome = () => {
  router.push({ name: 'home' })
}

const removeSection = (eraToRemove: string) => {
  const index = selectedEras.value.indexOf(eraToRemove)
  if (index > -1) {
    selectedEras.value.splice(index, 1)
    
    // Update URL to reflect the change
    if (selectedEras.value.length === 0) {
      // No sections left, go back to home
      goBack()
    } else {
      // Update URL with remaining sections
      router.replace({
        name: 'timeline',
        query: {
          sections: selectedEras.value,
          publisher: publisher.value
        }
      })
    }
  }
}
</script>

<style scoped>
.sub-timeline-page {
  min-height: 100vh;
  position: relative;
}

.timeline-placeholder {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.publisher-info {
  min-width: 120px;
  text-align: right;
}

.gap-2 > * {
  margin: 0.25rem;
}
</style>
