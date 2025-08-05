// Export all API clients from a single entry point
export { ApiClient } from './base'
export { AccountsClient } from './accounts'
export { BooksClient } from './books'
export { TimelineClient } from './timeline'
export { authApiClient } from './authClient'

// Import classes for creating instances
import { AccountsClient } from './accounts'
import { BooksClient } from './books'
import { TimelineClient } from './timeline'

// Create singleton instances for easy use
export const accountsClient = new AccountsClient()
export const booksClient = new BooksClient()
export const timelineClient = new TimelineClient()
