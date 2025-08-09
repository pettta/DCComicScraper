# Comics Timeline Database & Scripts

This directory contains all database files and management scripts for the Comics Timeline application.

## Directory Contents

### Database Files
- `comics_auth.db` - OAuth authentication database (SQLite)
- `*.json` - Timeline era data files
- `timeline.db` - Main timeline database (when created)

### Management Scripts
- `create_admin_user.py` - Create initial admin users
- `admin_user_manager.py` - Comprehensive admin user management
- `recreate_oauth_database.py` - Database schema recreation utility
- `migrate_json_data.py` - JSON to database migration utility
- `setup_timeline_database.py` - Timeline database setup

## Quick Start Guide

1. **Create your first admin user:**
   ```bash
   cd Database
   python create_admin_user.py
   ```

2. **Start the OAuth proxy:**
   ```bash
   cd ../Backend/comics-timeline-oauth-proxy
   python local_setup.py
   ```

3. **Test admin access:**
   ```bash
   cd ../../Database
   pip install -r requirements.txt
   python admin_user_manager.py -u [your-admin-username] -p [your-password]
   ```

## Scripts

### `recreate_oauth_database.py`

**⚠️ DANGEROUS OPERATION** - Completely deletes and recreates the OAuth database with the latest schema. This will **delete all user data** including admin accounts.

#### When to Use
- After database schema updates (new columns added to models)
- When database corruption occurs
- When starting fresh with a clean database

#### Features
- Safely stops any running OAuth server processes
- Backs up current working directory
- Creates fresh database with current schema including:
  - Users table with email verification support
  - Email verification tokens table  
  - JWT token blacklist table
- Interactive confirmation to prevent accidental data loss

#### Usage
```bash
python recreate_oauth_database.py
```

#### ⚠️ WARNING
This script will:
1. **DELETE all existing user accounts**
2. **DELETE all email verification tokens**
3. **DELETE all authentication tokens**
4. **Reset the database to empty state**

After running this script, you will need to:
1. **Create a new admin user** with `create_admin_user.py`
2. **Re-register all users** through the frontend

### `create_admin_user.py`

Creates the initial admin user for the OAuth proxy. **Run this first** before using any other admin tools.

#### Features
- Interactive user creation with validation
- Secure password input (hidden from terminal)
- Email format validation
- Username format validation
- Automatic database table creation
- **Creates database in OAuth proxy directory (not scripts folder)**

#### Usage

**Interactive mode (recommended):**
```bash
python create_admin_user.py
```

**With pre-filled username and email:**
```bash
python create_admin_user.py -u admin -e admin@example.com -p
```

#### Prerequisites
- OAuth proxy files must be available (../Backend/comics-timeline-oauth-proxy)
- No dependencies needed (uses only built-in Python modules)

### `admin_user_manager.py`

A comprehensive script for admin users to manage the OAuth proxy user database.

#### Features
- Login as admin user
- List all users in the system with email verification status
- Get detailed information about specific users including verification status
- View admin statistics (user counts, active/inactive users)
- **Promote users to admin status**
- **Demote users from admin status**
- **Activate/deactivate user accounts**
- **Verify/unverify user email addresses**
- Proper error handling and formatted output

#### Prerequisites

1. **Create admin user first:**
   ```bash
   python create_admin_user.py
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **OAuth proxy running:**
   Make sure the OAuth proxy is running on `localhost:8001`:
   ```bash
   cd ../Backend/comics-timeline-oauth-proxy
   python local_setup.py
   ```

#### Usage Examples

**List all users and statistics:**
```bash
python admin_user_manager.py -u admin -p your_password
```

**Show only statistics:**
```bash
python admin_user_manager.py -u admin -p your_password --stats-only
```

**Get specific user details:**
```bash
python admin_user_manager.py -u admin -p your_password --user-id 1
```

**Promote user to admin:**
```bash
python admin_user_manager.py -u admin -p your_password --promote 5
```

**Demote user from admin:**
```bash
python admin_user_manager.py -u admin -p your_password --demote 3
```

**Activate user account:**
```bash
python admin_user_manager.py -u admin -p your_password --activate 2
```

**Deactivate user account:**
```bash
python admin_user_manager.py -u admin -p your_password --deactivate 4
```

**Verify user email:**
```bash
python admin_user_manager.py -u admin -p your_password --verify-email 6
```

**Mark email as unverified:**
```bash
python admin_user_manager.py -u admin -p your_password --unverify-email 7
```

**Use different server:**
```bash
python admin_user_manager.py -u admin -p your_password --server http://localhost:9000
```

#### Sample Output

**User List:**
```
=============================================================================================
USER LIST
=============================================================================================
ID   Username             Email                          Active   Admin    Email Verified
---------------------------------------------------------------------------------------------
1    admin                admin@example.com              Yes      Yes      Yes
2    testuser             test@example.com               Yes      No       Yes
3    inactiveuser         inactive@example.com           No       No       No
=============================================================================================
```

**Statistics:**
```
========================================
ADMIN STATISTICS
========================================
Total Users: 3
Active Users: 2
Inactive Users: 1
Admin Users: 1
========================================
```

#### Error Handling

The script includes comprehensive error handling for:
- Network connection issues
- Authentication failures
- Permission denied (non-admin users)
- Invalid user IDs
- Server unavailable

#### Security Notes

- Always use strong passwords for admin accounts
- The script uses HTTPS if available
- Tokens are automatically logged out after use
- Sensitive information is not logged

## Adding More Scripts

To add new scripts:

1. Create the Python file in this directory
2. Add any new dependencies to `requirements.txt`
3. Update this README with usage instructions
4. Follow the same error handling and output formatting patterns
