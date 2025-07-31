import { ApiClient } from './base'
import type { LegendEra } from '../types/ui'

export class TimelineClient extends ApiClient {
  async getEras(publisher?: string, startYear?: number, endYear?: number): Promise<LegendEra[]> {
    const params = new URLSearchParams()
    if (publisher) params.append('publisher', publisher)
    if (startYear) params.append('start_year', startYear.toString())
    if (endYear) params.append('end_year', endYear.toString())
    
    const queryString = params.toString()
    const endpoint = `/timeline/eras${queryString ? `?${queryString}` : ''}`
    return await this.request<LegendEra[]>(endpoint)
  }
}
