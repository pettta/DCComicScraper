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

<template>
  <div class="app">
    <header>
      <h1>DC Comics Timeline</h1>
      <p>Explore the history and eras of DC Comics</p>
    </header>
    
    <main class="main-content">
      <div class="sidebar">
        <div v-if="loading" class="loading">
          Loading timeline data...
        </div>
        <div v-else-if="error" class="error">
          <p>Error loading data: {{ error }}</p>
        </div>
        <Legend v-else :legend-data="legendData" />
      </div>
      
      <div class="content">
        <Timeline v-if="!loading && !error" :legend-data="legendData" />
        <div v-else-if="loading" class="timeline-loading">
          Loading timeline...
        </div>
        <div v-else class="timeline-error">
          Timeline unavailable
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.app {
  min-height: 100vh;
  background-color: #ffffff;
}

header {
  text-align: center;
  padding: 2rem;
  background-color: #2c3e50;
  color: white;
  margin-bottom: 2rem;
}

header h1 {
  margin: 0 0 0.5rem 0;
  font-size: 2.5rem;
}

header p {
  margin: 0;
  font-size: 1.1rem;
  opacity: 0.9;
}

.main-content {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.sidebar {
  position: sticky;
  top: 2rem;
  height: fit-content;
}

.content {
  min-height: 80vh;
}

.loading {
  padding: 1rem;
  text-align: center;
  color: #666;
  font-style: italic;
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.error {
  padding: 1rem;
  background-color: #fee;
  border: 1px solid #fcc;
  border-radius: 8px;
  color: #c33;
}

.error p {
  margin: 0 0 1rem 0;
}

.retry-button {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.retry-button:hover {
  background-color: #c82333;
}

.timeline-loading, .timeline-error {
  padding: 2rem;
  text-align: center;
  color: #666;
  font-style: italic;
  background-color: #f8f9fa;
  border-radius: 8px;
  margin: 1rem 0;
}

.timeline-error {
  color: #c33;
  background-color: #fee;
}

/* Responsive design */
@media (max-width: 768px) {
  .main-content {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .sidebar {
    position: static;
  }
  
  header h1 {
    font-size: 2rem;
  }
}
</style>
