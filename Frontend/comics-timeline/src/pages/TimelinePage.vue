<template>
  <div class="timeline-page">
    <!-- Header -->
    <v-app-bar color="#2c3e50" dark elevation="0" height="120">
      <v-container class="d-flex justify-space-between align-center">
        
        <div class="text-center flex-grow-1">
          <h1 class="text-h3 mb-2">{{ selectedPublisher }} Comics Timeline</h1>
          <p class="text-h6 mb-0" style="opacity: 0.9;">Explore the history and eras of {{ selectedPublisher }} Comics</p>
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
    <v-main>
      <v-container fluid class="pa-4">
        <v-row>
          <v-col cols="12">
            <Timeline v-if="!loading && !error" :legend-data="legendData" />
            <v-card v-else-if="loading" class="pa-8 text-center">
              <v-progress-circular indeterminate color="primary"></v-progress-circular>
              <p class="mt-4 text-body-2 text-medium-emphasis">Loading {{ selectedPublisher }} timeline...</p>
            </v-card>
            <v-card v-else color="error" variant="tonal" class="pa-8 text-center">
              <p class="text-body-2">{{ selectedPublisher }} timeline unavailable</p>
            </v-card>
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

// Publisher selection
const publishers = ['DC', 'Marvel']
const selectedPublisher = ref<string>('DC')

// Define reactive legend data
const legendData = ref<LegendEra[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

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
  await fetchLegendData(newPublisher)
}

// Fetch data when component mounts
onMounted(async () => {
  await fetchLegendData(selectedPublisher.value)
})
</script>

<style scoped>
.publisher-selector {
  min-width: 150px;
}

.publisher-dropdown {
  max-width: 180px;
}

/* Ensure the dropdown has proper contrast on dark background */
:deep(.v-field--variant-outlined .v-field__outline) {
  --v-field-border-opacity: 0.6;
}

:deep(.v-field--variant-outlined.v-field--focused .v-field__outline) {
  --v-field-border-opacity: 1;
}
</style>
