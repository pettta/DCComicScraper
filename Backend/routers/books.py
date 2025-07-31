from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

router = APIRouter(
    prefix="/books",
    tags=["books"],
    responses={404: {"description": "Not found"}},
)

# Sample data - replace with actual database operations
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
    """Get all books"""
    return fake_books_db

@router.get("/{book_id}")
async def get_book(book_id: int) -> Dict[str, Any]:
    """Get a specific book by ID"""
    for book in fake_books_db:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@router.get("/era/{era_name}")
async def get_books_by_era(era_name: str) -> List[Dict[str, Any]]:
    """Get books filtered by era"""
    filtered_books = [book for book in fake_books_db if book["era"].lower() == era_name.lower()]
    if not filtered_books:
        raise HTTPException(status_code=404, detail=f"No books found for era: {era_name}")
    return filtered_books

@router.get("/series/{series_name}")
async def get_books_by_series(series_name: str) -> List[Dict[str, Any]]:
    """Get books filtered by series"""
    filtered_books = [book for book in fake_books_db if series_name.lower() in book["series"].lower()]
    if not filtered_books:
        raise HTTPException(status_code=404, detail=f"No books found for series: {series_name}")
    return filtered_books

@router.post("/")
async def create_book(book: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new book entry"""
    new_book = {
        "id": len(fake_books_db) + 1,
        **book
    }
    fake_books_db.append(new_book)
    return new_book

@router.put("/{book_id}")
async def update_book(book_id: int, book: Dict[str, Any]) -> Dict[str, Any]:
    """Update an existing book"""
    for i, existing_book in enumerate(fake_books_db):
        if existing_book["id"] == book_id:
            updated_book = {**existing_book, **book}
            fake_books_db[i] = updated_book
            return updated_book
    raise HTTPException(status_code=404, detail="Book not found")

@router.delete("/{book_id}")
async def delete_book(book_id: int) -> Dict[str, str]:
    """Delete a book"""
    for i, book in enumerate(fake_books_db):
        if book["id"] == book_id:
            del fake_books_db[i]
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")
