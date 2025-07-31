<template>
  <div class="timeline">
    <h3>Comics Timeline</h3>
    <v-timeline
      direction="horizontal"
      density="comfortable"
      line-inset="12"
    >
      <v-timeline-item
        v-for="(era, index) in props.legendData"
        :key="index"
        :dot-color="getColorForIndex(index)"
        size="small"
      >
        <template v-slot:icon>
          <v-icon size="small">mdi-calendar</v-icon>
        </template>
        
        <v-card>
          <v-card-title :style="{ color: getColorForIndex(index) }">
            {{ era.title }}
          </v-card-title>
          
          <v-card-subtitle>
            {{ era.ending_event || 'Ongoing' }}
          </v-card-subtitle>

          <v-card-subtitle>
            {{ era.years[0] }} - {{ era.years[1] }}
          </v-card-subtitle>
          
          <v-card-text>
            {{ era.description }}
          </v-card-text>
        </v-card>
      </v-timeline-item>
    </v-timeline>
  </div>
</template>

<script setup lang="ts">
import type { LegendEra } from '../types/ui'

interface Props {
  legendData: LegendEra[]
}

const props = defineProps<Props>()

// Color palette to match the Legend component
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
.timeline {
  padding: 1rem;
  width: 100%;
}

.timeline h3 {
  margin: 0 0 2rem 0;
  color: #333;
  font-size: 1.5rem;
  text-align: center;
}
</style>
