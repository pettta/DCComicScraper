# Comics Timeline OAuth2 Proxy

A FastAPI-based OAuth2 authentication service with JWT tokens and SQLite database for the Comics Timeline application.

## Features

- **JWT Authentication**: Secure token-based authentication
- **SQLite Database**: Lightweight database for user management
- **User Registration & Login**: Complete authentication flow
- **Admin Panel**: Administrative user management
- **Token Blacklisting**: Secure logout functionality
- **Password Management**: Change passwords securely
- **CORS Support**: Frontend integration ready

## Quick Start

1. **Install Dependencies**:
   ```bash
   python local_setup.py
   ```

2. **Manual Setup** (alternative):
   ```bash
   pip install -r requirements.txt
   python main.py
   ```

3. **Access the API**:
   - API Documentation: http://localhost:8001/docs
   - Health Check: http://localhost:8001/health

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `POST /auth/logout` - Logout user
- `GET /auth/me` - Get current user info
- `POST /auth/change-password` - Change password
- `GET /auth/verify-token` - Verify token validity

### Admin (Requires admin privileges)
- `GET /admin/users` - List all users
- `GET /admin/users/{user_id}` - Get specific user
- `POST /admin/users` - Create user (with admin privileges)
- `PUT /admin/users/{user_id}` - Update user
- `DELETE /admin/users/{user_id}` - Delete user
- `GET /admin/stats` - Get user statistics

### Protected Routes
- `GET /protected` - Test protected endpoint

## Environment Variables

Create a `.env` file with:
```
SECRET_KEY=your-super-secret-key-change-this-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///../../Database/comics_auth.db
```

## Database

The application automatically creates a SQLite database (`comics_auth.db`) in the centralized `Database` directory with the following tables:
- `users` - User accounts and profiles with email verification support
- `email_verifications` - Email verification tokens
- `token_blacklist` - Revoked tokens

## Usage Example

1. **Register a user**:
   ```bash
   curl -X POST "http://localhost:8001/auth/register" \
        -H "Content-Type: application/json" \
        -d '{"username": "testuser", "email": "test@example.com", "password": "testpass123"}'
   ```

2. **Login**:
   ```bash
   curl -X POST "http://localhost:8001/auth/login" \
        -H "Content-Type: application/json" \
        -d '{"username": "testuser", "password": "testpass123"}'
   ```

3. **Access protected endpoints**:
   ```bash
   curl -X GET "http://localhost:8001/auth/me" \
        -H "Authorization: Bearer YOUR_TOKEN_HERE"
   ```

## Integration

This OAuth2 proxy is designed to work alongside the main Comics Timeline backend. Configure your main application to verify tokens using the `/auth/verify-token` endpoint.

## Security

- Passwords are hashed using bcrypt
- JWT tokens include expiration times
- Tokens can be blacklisted for secure logout
- Admin-only endpoints are protected
- CORS is configured for frontend integration
