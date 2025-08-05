from fastapi import APIRouter
from typing import List, Dict, Any

router = APIRouter(
    prefix="/books",
    tags=["books"],
    responses={404: {"description": "Not found"}},
)

# Sample data - TODO replace with actual database operations
fake_books_db = [
    {
        "id": 1,
        "title": "Action Comics #1",
        "series": "Action Comics",
        "issue_number": 1,
        "year": 1938,
        "era": "Pre-Crisis",
        "price": 3000000.00,
        "condition": "Good"
    },
    {
        "id": 2,
        "title": "Batman #1",
        "series": "Batman",
        "issue_number": 1,
        "year": 1940,
        "era": "Pre-Crisis",
        "price": 567000.00,
        "condition": "Very Fine"
    },
    {
        "id": 3,
        "title": "Crisis on Infinite Earths #1",
        "series": "Crisis on Infinite Earths",
        "issue_number": 1,
        "year": 1985,
        "era": "Post-Crisis",
        "price": 25.00,
        "condition": "Near Mint"
    }
]

@router.get("/")
async def get_books() -> List[Dict[str, Any]]:
    return fake_books_db
