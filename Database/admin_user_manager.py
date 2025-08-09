import argparse
import requests
import json
import sys
from typing import Optional, Dict, Any, List

class OAuthAdminClient:
    """Client for interacting with the OAuth proxy as an admin user"""
    
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.session = requests.Session()
        self.token: Optional[str] = None
        
    def login(self, username: str, password: str) -> bool:
        """Login and obtain access token"""
        try:
            response = self.session.post(
                f"{self.base_url}/auth/login",
                json={"username": username, "password": password}
            )
            response.raise_for_status()
            
            data = response.json()
            self.token = data["access_token"]
            
            # Set authorization header for future requests
            self.session.headers.update({
                "Authorization": f"Bearer {self.token}"
            })
            
            print(f"✅ Successfully logged in as: {username}")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Login failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json().get('detail', 'Unknown error')
                    print(f"   Error details: {error_detail}")
                except:
                    print(f"   HTTP Status: {e.response.status_code}")
            return False
    
    def verify_admin_access(self) -> bool:
        """Verify that the current user has admin privileges"""
        try:
            response = self.session.get(f"{self.base_url}/auth/me")
            response.raise_for_status()
            
            user_data = response.json()
            if user_data.get("is_admin", False):
                print(f"✅ Admin access confirmed for user: {user_data['username']}")
                return True
            else:
                print(f"❌ User {user_data['username']} does not have admin privileges")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to verify admin access: {e}")
            return False
    
    def get_all_users(self) -> Optional[List[Dict[str, Any]]]:
        """Get list of all users (admin only)"""
        try:
            response = self.session.get(f"{self.base_url}/admin/users")
            response.raise_for_status()
            
            users = response.json()
            print(f"✅ Retrieved {len(users)} users")
            return users
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to get users: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"   HTTP Status: {e.response.status_code}")
                if e.response.status_code == 403:
                    print("   This operation requires admin privileges")
            return None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get specific user by ID (admin only)"""
        try:
            response = self.session.get(f"{self.base_url}/admin/users/{user_id}")
            response.raise_for_status()
            
            user = response.json()
            print(f"✅ Retrieved user: {user['username']}")
            return user
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to get user {user_id}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"   HTTP Status: {e.response.status_code}")
                if e.response.status_code == 404:
                    print(f"   User with ID {user_id} not found")
            return None
    
    def get_admin_stats(self) -> Optional[Dict[str, Any]]:
        """Get admin statistics (admin only)"""
        try:
            response = self.session.get(f"{self.base_url}/admin/stats")
            response.raise_for_status()
            
            stats = response.json()
            print("✅ Retrieved admin statistics")
            return stats
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to get admin stats: {e}")
            return None
    
    def update_user_permissions(self, user_id: int, is_admin: bool = None, is_active: bool = None, is_email_verified: bool = None) -> Optional[Dict[str, Any]]:
        """Update user permissions (admin only)"""
        try:
            update_data = {}
            if is_admin is not None:
                update_data["is_admin"] = is_admin
            if is_active is not None:
                update_data["is_active"] = is_active
            if is_email_verified is not None:
                update_data["is_email_verified"] = is_email_verified
            
            if not update_data:
                print("❌ No updates provided")
                return None
            
            response = self.session.put(f"{self.base_url}/admin/users/{user_id}", json=update_data)
            response.raise_for_status()
            
            user = response.json()
            print(f"✅ Updated user {user['username']} permissions")
            return user
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to update user {user_id}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"   HTTP Status: {e.response.status_code}")
                if e.response.status_code == 404:
                    print(f"   User with ID {user_id} not found")
                elif e.response.status_code == 400:
                    try:
                        error_detail = e.response.json().get('detail', 'Bad request')
                        print(f"   Error: {error_detail}")
                    except:
                        pass
            return None
    
    def promote_to_admin(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Promote user to admin status"""
        print(f"🔼 Promoting user {user_id} to admin...")
        return self.update_user_permissions(user_id, is_admin=True)
    
    def demote_from_admin(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Demote user from admin status"""
        print(f"🔽 Demoting user {user_id} from admin...")
        return self.update_user_permissions(user_id, is_admin=False)
    
    def activate_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Activate user account"""
        print(f"✅ Activating user {user_id}...")
        return self.update_user_permissions(user_id, is_active=True)
    
    def deactivate_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Deactivate user account"""
        print(f"❌ Deactivating user {user_id}...")
        return self.update_user_permissions(user_id, is_active=False)
    
    def verify_user_email(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Mark user's email as verified"""
        print(f"✅ Verifying email for user {user_id}...")
        return self.update_user_permissions(user_id, is_email_verified=True)
    
    def unverify_user_email(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Mark user's email as unverified"""
        print(f"❌ Marking email as unverified for user {user_id}...")
        return self.update_user_permissions(user_id, is_email_verified=False)
    
    def logout(self):
        """Logout and invalidate token"""
        if self.token:
            try:
                self.session.post(f"{self.base_url}/auth/logout")
                print("✅ Successfully logged out")
            except:
                pass  # Logout endpoint might fail, but we clear local token anyway
            
            self.token = None
            self.session.headers.pop("Authorization", None)

def print_user_table(users: List[Dict[str, Any]]):
    """Print users in a formatted table"""
    if not users:
        print("No users found.")
        return
    
    print("\n" + "="*95)
    print("USER LIST")
    print("="*95)
    print(f"{'ID':<4} {'Username':<20} {'Email':<30} {'Active':<8} {'Admin':<8} {'Email Verified':<15}")
    print("-"*95)
    
    for user in users:
        email_verified = user.get('is_email_verified', False)
        print(f"{user['id']:<4} "
              f"{user['username']:<20} "
              f"{user['email']:<30} "
              f"{'Yes' if user['is_active'] else 'No':<8} "
              f"{'Yes' if user['is_admin'] else 'No':<8} "
              f"{'Yes' if email_verified else 'No':<15}")
    
    print("="*95)

def print_user_details(user: Dict[str, Any]):
    """Print detailed user information"""
    print("\n" + "="*50)
    print("USER DETAILS")
    print("="*50)
    print(f"ID: {user['id']}")
    print(f"Username: {user['username']}")
    print(f"Email: {user['email']}")
    print(f"Active: {'Yes' if user['is_active'] else 'No'}")
    print(f"Admin: {'Yes' if user['is_admin'] else 'No'}")
    print(f"Email Verified: {'Yes' if user.get('is_email_verified', False) else 'No'}")
    print(f"Created: {user['created_at']}")
    if user.get('last_login'):
        print(f"Last Login: {user['last_login']}")
    else:
        print("Last Login: Never")
    print("="*50)

def print_stats(stats: Dict[str, Any]):
    """Print admin statistics"""
    print("\n" + "="*40)
    print("ADMIN STATISTICS")
    print("="*40)
    print(f"Total Users: {stats['total_users']}")
    print(f"Active Users: {stats['active_users']}")
    print(f"Inactive Users: {stats['inactive_users']}")
    print(f"Admin Users: {stats['admin_users']}")
    print("="*40)

def main():
    parser = argparse.ArgumentParser(
        description="Admin User Management for Comics Timeline OAuth Proxy",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python admin_user_manager.py -u admin -p password123
  python admin_user_manager.py -u admin -p password123 --stats-only
  python admin_user_manager.py -u admin -p password123 --user-id 1
  python admin_user_manager.py -u admin -p password123 --promote 5
  python admin_user_manager.py -u admin -p password123 --demote 3
  python admin_user_manager.py -u admin -p password123 --activate 2
  python admin_user_manager.py -u admin -p password123 --deactivate 4
  python admin_user_manager.py -u admin -p password123 --verify-email 6
  python admin_user_manager.py -u admin -p password123 --unverify-email 7
  python admin_user_manager.py -u admin -p password123 --server http://localhost:8001
        """
    )
    
    parser.add_argument('-u', '--username', required=True,
                        help='Admin username')
    parser.add_argument('-p', '--password', required=True,
                        help='Admin password')
    parser.add_argument('--user-id', type=int,
                        help='Get specific user by ID')
    parser.add_argument('--stats-only', action='store_true',
                        help='Only show admin statistics')
    parser.add_argument('--promote', type=int, metavar='USER_ID',
                        help='Promote user to admin status')
    parser.add_argument('--demote', type=int, metavar='USER_ID',
                        help='Demote user from admin status')
    parser.add_argument('--activate', type=int, metavar='USER_ID',
                        help='Activate user account')
    parser.add_argument('--deactivate', type=int, metavar='USER_ID',
                        help='Deactivate user account')
    parser.add_argument('--verify-email', type=int, metavar='USER_ID',
                        help='Mark user email as verified')
    parser.add_argument('--unverify-email', type=int, metavar='USER_ID',
                        help='Mark user email as unverified')
    parser.add_argument('--server', default='http://localhost:8001',
                        help='OAuth proxy server URL (default: http://localhost:8001)')
    
    args = parser.parse_args()
    
    # Create client and login
    client = OAuthAdminClient(args.server)
    
    print(f"🔗 Connecting to OAuth proxy: {args.server}")
    print(f"👤 Attempting login as: {args.username}")
    
    if not client.login(args.username, args.password):
        sys.exit(1)
    
    # Verify admin access
    if not client.verify_admin_access():
        client.logout()
        sys.exit(1)
    
    try:
        # Handle permission changes
        if args.promote:
            user = client.promote_to_admin(args.promote)
            if user:
                print_user_details(user)
        
        elif args.demote:
            user = client.demote_from_admin(args.demote)
            if user:
                print_user_details(user)
        
        elif args.activate:
            user = client.activate_user(args.activate)
            if user:
                print_user_details(user)
        
        elif args.deactivate:
            user = client.deactivate_user(args.deactivate)
            if user:
                print_user_details(user)
        
        elif args.verify_email:
            user = client.verify_user_email(args.verify_email)
            if user:
                print_user_details(user)
        
        elif args.unverify_email:
            user = client.unverify_user_email(args.unverify_email)
            if user:
                print_user_details(user)
        
        # Handle specific user request
        elif args.user_id:
            user = client.get_user_by_id(args.user_id)
            if user:
                print_user_details(user)
        
        # Handle stats only request
        elif args.stats_only:
            stats = client.get_admin_stats()
            if stats:
                print_stats(stats)
        
        # Default: show all users and stats
        else:
            # Get and display all users
            users = client.get_all_users()
            if users:
                print_user_table(users)
            
            # Get and display stats
            stats = client.get_admin_stats()
            if stats:
                print_stats(stats)
    
    finally:
        # Always logout
        client.logout()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
