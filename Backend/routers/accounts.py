from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
    responses={404: {"description": "Not found"}},
)

# Sample data - replace with actual database operations
fake_accounts_db = [
    {"id": 1, "username": "admin", "email": "admin@example.com", "is_active": True},
    {"id": 2, "username": "user1", "email": "user1@example.com", "is_active": True},
]

@router.get("/")
async def get_accounts() -> List[Dict[str, Any]]:
    """Get all accounts"""
    return fake_accounts_db

@router.get("/{account_id}")
async def get_account(account_id: int) -> Dict[str, Any]:
    """Get a specific account by ID"""
    for account in fake_accounts_db:
        if account["id"] == account_id:
            return account
    raise HTTPException(status_code=404, detail="Account not found")

@router.post("/")
async def create_account(account: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new account"""
    # In a real app, you'd validate the input and save to database
    new_account = {
        "id": len(fake_accounts_db) + 1,
        **account,
        "is_active": True
    }
    fake_accounts_db.append(new_account)
    return new_account

@router.put("/{account_id}")
async def update_account(account_id: int, account: Dict[str, Any]) -> Dict[str, Any]:
    """Update an existing account"""
    for i, existing_account in enumerate(fake_accounts_db):
        if existing_account["id"] == account_id:
            updated_account = {**existing_account, **account}
            fake_accounts_db[i] = updated_account
            return updated_account
    raise HTTPException(status_code=404, detail="Account not found")

@router.delete("/{account_id}")
async def delete_account(account_id: int) -> Dict[str, str]:
    """Delete an account"""
    for i, account in enumerate(fake_accounts_db):
        if account["id"] == account_id:
            del fake_accounts_db[i]
            return {"message": "Account deleted successfully"}
    raise HTTPException(status_code=404, detail="Account not found")
