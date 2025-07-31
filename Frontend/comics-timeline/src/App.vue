<script setup lang="ts">
import { ref } from 'vue'
import Legend from './components/Legend.vue'
import Timeline from './components/Timeline.vue'
import type { LegendEra } from './types/ui'

// Define the legend data at the app level
const legendData = ref<LegendEra[]>([
  {
    title: "Pre-Crisis",
    years: [1938, 1985],
    description: "Beginning of DC Comics up to the beginning of the modern age"
  },
  {
    title: "Post-Crisis",
    years: [1985, 2011],
    description: "Modern age following Crisis on Infinite Earths through Flashpoint"
  },
  {
    title: "New 52",
    years: [2011, 2016],
    description: "DC Universe reboot following Flashpoint event"
  },
  {
    title: "Rebirth",
    years: [2016, 2024],
    description: "Soft reboot bringing back classic elements to DC continuity"
  }
])
</script>

<template>
  <div class="app">
    <header>
      <h1>DC Comics Timeline</h1>
      <p>Explore the history and eras of DC Comics</p>
    </header>
    
    <main class="main-content">
      <div class="sidebar">
        <Legend :legend-data="legendData" />
      </div>
      
      <div class="content">
        <Timeline />
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
