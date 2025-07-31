<template>
  <v-app>
    <!-- Header using Vuetify -->
    <v-app-bar color="#2c3e50" dark elevation="0" height="120">
      <v-container class="text-center">
        <h1 class="text-h3 mb-2">DC Comics Timeline</h1>
        <p class="text-h6 mb-0" style="opacity: 0.9;">Explore the history and eras of DC Comics</p>
      </v-container>
    </v-app-bar>

    <v-main>
      <v-container fluid class="pa-4">
        <!-- Full width timeline -->
        <v-row>
          <v-col cols="12">
            <Timeline v-if="!loading && !error" :legend-data="legendData" />
            
            <v-card v-else-if="loading" class="pa-8 text-center">
              <v-progress-circular indeterminate color="primary"></v-progress-circular>
              <p class="mt-4 text-body-2 text-medium-emphasis">Loading timeline...</p>
            </v-card>
            
            <v-card v-else color="error" variant="tonal" class="pa-8 text-center">
              <p class="text-body-2">Timeline unavailable</p>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<style scoped>
/* Only keep minimal CSS that Vuetify doesn't provide */
.sticky-sidebar {
  position: sticky;
  top: 2rem;
}

/* Responsive adjustment for mobile */
@media (max-width: 960px) {
  .sticky-sidebar {
    position: static;
  }
}
</style>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { timelineClient } from './clients'
import type { LegendEra } from './types/ui'
import Legend from './components/Legend.vue'
import Timeline from './components/Timeline.vue'

// Define reactive legend data
const legendData = ref<LegendEra[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

const fetchLegendData = async (publisher: string='DC') => {
  loading.value = true
  error.value = null
  const response = await timelineClient.getEras(publisher)
  if (!response) {
    error.value = 'Failed to load legend data'
    loading.value = false
    return
  }  
  legendData.value = response
  loading.value = false
}


// Fetch data when component mounts
onMounted(async () => {
  await fetchLegendData('DC')
})

</script>
