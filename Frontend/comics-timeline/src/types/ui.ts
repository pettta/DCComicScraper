// UI-related TypeScript interfaces for the Comics Timeline application

export interface LegendEra {
  id: number 
  title: string
  years: [number, number]
  description: string
}

export interface TimelineEvent {
  id: number
  title: string
  date: string
  description: string
  color: string
}

// Add more UI-related interfaces here as the application grows
