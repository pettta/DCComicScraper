<template>
  <div class="legend">
    <h3>Legend</h3>
    <div class="legend-items">
      <div 
        class="legend-item" 
        v-for="(era, index) in legendData" 
        :key="index"
        :title="era.description"
      >
        <div 
          class="legend-color" 
          :style="{ backgroundColor: getColorForIndex(index) }"
        ></div>
        <span class="legend-label">
          {{ era.title }} ({{ era.years[0] }}-{{ era.years[1] }})
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { LegendEra } from '../types/ui'

interface Props {
  legendData: LegendEra[]
}

const props = defineProps<Props>()

// Color palette for different eras
const colors = [
  '#ff6b6b', // Red
  '#4ecdc4', // Teal
  '#45b7d1', // Blue
  '#96ceb4', // Green
  '#ffeaa7', // Yellow
  '#fd79a8', // Pink
  '#a29bfe', // Purple
  '#fd6c6c'  // Light Red
]

const getColorForIndex = (index: number): string => {
  return colors[index % colors.length]
}
</script>

<style scoped>
.legend {
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.legend h3 {
  margin: 0 0 1rem 0;
  color: #333;
  font-size: 1.2rem;
}

.legend-items {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.legend-color {
  width: 20px;
  height: 20px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.legend-label {
  font-size: 0.9rem;
  color: #555;
}
</style>
