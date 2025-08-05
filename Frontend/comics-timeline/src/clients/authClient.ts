class AuthApiClient {
  private baseURL: string

  constructor(baseURL: string = 'http://localhost:8001') {
    this.baseURL = baseURL
  }

  private async request(endpoint: string, options: RequestInit = {}): Promise<any> {
    const token = localStorage.getItem('auth_token')
    
    const config: RequestInit = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
        ...(token && { Authorization: `Bearer ${token}` })
      }
    }

    const response = await fetch(`${this.baseURL}${endpoint}`, config)
    
    if (response.status === 401) {
      localStorage.removeItem('auth_token')
    }

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Request failed' }))
      throw { response: { status: response.status, data: error } }
    }

    return response.json()
  }

  async login(username: string, password: string) {
    return this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password })
    })
  }

  async register(username: string, email: string, password: string) {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ username, email, password })
    })
  }

  async logout() {
    return this.request('/auth/logout', {
      method: 'POST'
    })
  }

  async getCurrentUser() {
    return this.request('/auth/me')
  }

  async verifyToken() {
    return this.request('/auth/verify-token')
  }

  async changePassword(currentPassword: string, newPassword: string) {
    return this.request('/auth/change-password', {
      method: 'POST',
      body: JSON.stringify({
        current_password: currentPassword,
        new_password: newPassword
      })
    })
  }

  setAuthToken(token: string) {
    localStorage.setItem('auth_token', token)
  }

  clearAuthToken() {
    localStorage.removeItem('auth_token')
  }
}

export const authApiClient = new AuthApiClient()
