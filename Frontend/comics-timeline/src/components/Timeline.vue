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
        
        <v-card 
          class="timeline-card"
          :class="{ 'card-hovered': hoveredCard === index }"
          @mouseenter="onCardHover(era, index)"
          @mouseleave="onCardLeave"
        >
          <div 
            v-if="hoveredCard === index && backgroundImage"
            class="card-background-image"
            :style="{ backgroundImage: `url(${backgroundImage})` }"
          ></div>
          
          <div class="card-content">
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
          </div>
        </v-card>
      </v-timeline-item>
    </v-timeline>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import type { LegendEra } from '../types/ui'

// Import timeline-specific styles
import '../styles/timeline.css'

// Import dynamic image asset manager
import { getEventImage } from '../utils/imageAssets'

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
            ],
            hoveredCard: null as number | null,
            backgroundImage: null as string | null
        }
    },
    methods: {
        getColorForIndex(index: number): string {
            return this.colors[index % this.colors.length]
        },
        
        async onCardHover(era: LegendEra, index: number) {
            this.hoveredCard = index
            
            // Get image for the ending event using the dynamic image system
            if (era.ending_event) {
                const imageUrl = getEventImage(era.ending_event)
                this.backgroundImage = imageUrl
                
                // Debug logging
                if (imageUrl) {
                    console.log(`Found image for "${era.ending_event}":`, imageUrl)
                } else {
                    console.log(`No image found for "${era.ending_event}"`)
                }
            }
        },
        
        onCardLeave() {
            this.hoveredCard = null
            this.backgroundImage = null
        }
    }
})
</script>


