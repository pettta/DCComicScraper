<template>
  <div class="timeline">
    <h3>Comics Timeline</h3>
    <div class="timeline-container">
      <div class="timeline-line"></div>
      
      <!-- Timeline events will go here -->
      <div class="timeline-event" v-for="event in timelineEvents" :key="event.id">
        <div class="timeline-marker" :style="{ backgroundColor: event.color }"></div>
        <div class="timeline-content">
          <h4>{{ event.title }}</h4>
          <p class="timeline-date">{{ event.date }}</p>
          <p class="timeline-description">{{ event.description }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { TimelineEvent } from '../types/ui'

// Sample timeline events - replace with actual data
const timelineEvents = ref<TimelineEvent[]>([
  {
    id: 1,
    title: "Crisis on Infinite Earths",
    date: "1985",
    description: "The event that ended the Pre-Crisis era and started Post-Crisis continuity.",
    color: "#ff6b6b"
  },
  {
    id: 2,
    title: "Flashpoint",
    date: "2011",
    description: "The event that led to the New 52 reboot of the DC Universe.",
    color: "#4ecdc4"
  },
  {
    id: 3,
    title: "DC Rebirth",
    date: "2016",
    description: "The soft reboot that brought back classic elements to DC continuity.",
    color: "#45b7d1"
  }
])
</script>

<style scoped>
.timeline {
  padding: 1rem;
}

.timeline h3 {
  margin: 0 0 2rem 0;
  color: #333;
  font-size: 1.5rem;
  text-align: center;
}

.timeline-container {
  position: relative;
  max-width: 800px;
  margin: 0 auto;
}

.timeline-line {
  position: absolute;
  left: 30px;
  top: 0;
  bottom: 0;
  width: 2px;
  background-color: #ddd;
}

.timeline-event {
  position: relative;
  margin-bottom: 2rem;
  padding-left: 80px;
}

.timeline-marker {
  position: absolute;
  left: 20px;
  top: 0;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 3px solid white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.timeline-content {
  background-color: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.timeline-content h4 {
  margin: 0 0 0.5rem 0;
  color: #333;
  font-size: 1.2rem;
}

.timeline-date {
  margin: 0 0 1rem 0;
  color: #666;
  font-weight: bold;
  font-size: 0.9rem;
}

.timeline-description {
  margin: 0;
  color: #555;
  line-height: 1.5;
}

/* Responsive design */
@media (max-width: 768px) {
  .timeline-event {
    padding-left: 60px;
  }
  
  .timeline-marker {
    left: 15px;
    width: 15px;
    height: 15px;
  }
  
  .timeline-line {
    left: 22px;
  }
}
</style>
