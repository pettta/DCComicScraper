<template>
  <div class="timeline-page">
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
        
        <div class="text-center flex-grow-1">
          <h1 class="text-h3 mb-2 header-title">{{ selectedPublisher }} Comics Timeline</h1>
          <p class="text-h6 mb-0 header-subtitle">Explore the history and eras of {{ selectedPublisher }} Comics</p>
        </div>
        
        <div class="publisher-selector">
          <v-select
            v-model="selectedPublisher"
            :items="publishers"
            label="Publisher"
            variant="outlined"
            density="comfortable"
            hide-details
            class="publisher-dropdown"
            dark
            @update:model-value="onPublisherChange"
          ></v-select>
        </div>
      </v-container>
    </v-app-bar>

    <!-- Main Content -->
    <v-main class="main-content">
      <v-container fluid class="pa-8 content-container">
        <v-row>
          <v-col cols="12">
            <!-- Selected Eras Display -->
            <v-card 
              v-if="selectedEras.length > 0" 
              class="mb-4 pa-4 selected-eras-card" 
              elevation="4"
            >
              <v-card-title class="text-h6 pb-2">
                Selected Eras ({{ selectedEras.length }})
              </v-card-title>
              
              <div class="d-flex flex-wrap gap-2 mb-3">
                <v-chip
                  v-for="era in selectedEras"
                  :key="era"
                  color="primary"
                  variant="elevated"
                  closable
                  @click:close="removeSelectedEra(era)"
                >
                  {{ era }}
                </v-chip>
              </div>
              
              <!-- Warning message -->
              <v-alert
                v-if="selectedEras.length > 1"
                type="warning"
                variant="tonal"
                density="compact"
                class="mb-3"
                icon="mdi-alert-circle-outline"
              >
                Having more than one section enabled might disable certain filters
              </v-alert>
              
              <!-- Load button -->
              <div class="d-flex justify-end">
                <v-btn
                  color="primary"
                  variant="elevated"
                  @click="loadCurrentSections"
                  :disabled="loading"
                >
                  <v-icon left>mdi-download</v-icon>
                  Load Current Sections
                </v-btn>
              </div>
            </v-card>
            
            <div class="timeline-wrapper">
              <Timeline 
                v-if="!loading && !error" 
                :legend-data="legendData" 
                @era-selection-changed="onEraSelectionChanged"
              />
              <v-card v-else-if="loading" class="pa-8 text-center loading-card" elevation="8">
                <v-progress-circular indeterminate color="primary" size="60"></v-progress-circular>
                <p class="mt-4 text-h6 text-medium-emphasis">Loading {{ selectedPublisher }} timeline...</p>
              </v-card>
              <v-card v-else color="error" variant="tonal" class="pa-8 text-center error-card" elevation="8">
                <v-icon icon="mdi-alert-circle" size="48" class="mb-4"></v-icon>
                <p class="text-h6">{{ selectedPublisher }} timeline unavailable</p>
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
import { timelineClient } from '../clients'
import type { LegendEra } from '../types/ui'
import Timeline from '../components/Timeline.vue'

// Import modular styles
import '../styles/index.css'

// Publisher selection
const publishers = ['DC', 'Marvel']
const selectedPublisher = ref<string>('DC')

// Define reactive legend data
const legendData = ref<LegendEra[]>([])
const loading = ref(true)
const error = ref<string | null>(null)
const selectedEras = ref<string[]>([])

const fetchLegendData = async (publisher: string) => {
  loading.value = true
  error.value = null
  
  try {
    const response = await timelineClient.getEras(publisher)
    if (!response || response.length === 0) {
      error.value = `No timeline data found for ${publisher}`
      legendData.value = []
    } else {
      legendData.value = response
    }
  } catch (err) {
    error.value = `Failed to load ${publisher} timeline data`
    console.error('Error fetching timeline data:', err)
    legendData.value = []
  } finally {
    loading.value = false
  }
}

// Handle publisher change
const onPublisherChange = async (newPublisher: string) => {
  console.log(`Publisher changed to: ${newPublisher}`)
  selectedEras.value = [] // Clear selections when publisher changes
  await fetchLegendData(newPublisher)
}

// Handle era selection changes
const onEraSelectionChanged = (newSelectedEras: string[]) => {
  selectedEras.value = newSelectedEras
  console.log('Era selection updated:', newSelectedEras)
}

// Remove a specific era from selection
const removeSelectedEra = (eraToRemove: string) => {
  const index = selectedEras.value.indexOf(eraToRemove)
  if (index > -1) {
    selectedEras.value.splice(index, 1)
    console.log('Removed era:', eraToRemove)
  }
}

// Load current sections
const loadCurrentSections = async () => {
  if (selectedEras.value.length === 0) {
    console.warn('No eras selected to load')
    return
  }

  console.log('Loading current sections:', selectedEras.value)
  
  // TODO: Implement the actual loading logic here
  // This could involve:
  // - Fetching specific data for the selected eras
  // - Applying filters based on the selections
  // - Navigating to a different view
  // - Updating the application state
  
  // For now, just show a confirmation
  // You can replace this with actual implementation
  alert(`Loading ${selectedEras.value.length} selected era(s): ${selectedEras.value.join(', ')}`)
}

// Fetch data when component mounts
onMounted(async () => {
  await fetchLegendData(selectedPublisher.value)
})
</script>


