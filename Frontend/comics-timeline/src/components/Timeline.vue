<template>
  <div class="timeline">
    <v-timeline
      direction="horizontal"
      density="comfortable"
      line-inset="12"
    >
      <v-timeline-item
        v-for="(era, index) in legendData"
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

<script lang="ts">
import { defineComponent } from 'vue'
import type { LegendEra } from '../types/ui'

export default defineComponent({
    name: 'Timeline',
    props: {
        legendData: {
            type: Array as () => LegendEra[],
            required: true
        }
    },
    data() {
        return {
            colors: [
                '#ff6b6b', // Red
                '#4ecdc4', // Teal
                '#45b7d1', // Blue
                '#96ceb4', // Green
                '#ffeaa7', // Yellow
                '#fd79a8', // Pink
                '#a29bfe', // Purple
                '#fd6c6c'  // Light Red
            ]
        }
    },
    methods: {
        getColorForIndex(index: number): string {
            return this.colors[index % this.colors.length]
        }
    }
})
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
