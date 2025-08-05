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
          :class="{ 
            'card-hovered': hoveredCard === index,
            'card-selected': selectedEras.includes(era.title)
          }"
          @mouseenter="onCardHover(era, index)"
          @mouseleave="onCardLeave"
          @click="onCardClick(era)"
        >
          <div 
            v-if="hoveredCard === index && backgroundImage"
            class="card-background-image"
            :style="{ backgroundImage: `url(${backgroundImage})` }"
          ></div>
          
          <!-- Selection indicator -->
          <div 
            v-if="selectedEras.includes(era.title)"
            class="card-selection-indicator"
          >
            <v-icon icon="mdi-check-circle" size="24" color="success"></v-icon>
          </div>
          
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
    emits: ['era-selection-changed'],
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
            backgroundImage: null as string | null,
            selectedEras: [] as string[]
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
        },

        onCardClick(era: LegendEra) {
            const eraTitle = era.title
            const index = this.selectedEras.indexOf(eraTitle)
            
            if (index > -1) {
                // Era is already selected, remove it
                this.selectedEras.splice(index, 1)
            } else {
                // Era is not selected, add it
                this.selectedEras.push(eraTitle)
            }
            
            // Emit the updated selection to parent component
            this.$emit('era-selection-changed', [...this.selectedEras])
            
            // Debug logging
            console.log('Selected eras:', this.selectedEras)
        }
    }
})
</script>


