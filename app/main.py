from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn
import os

from app import crud, models, schemas
from app.database import SessionLocal, engine, get_db

# Create all tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Library Management System API",
    description="A comprehensive CRUD API for managing library operations including books, members, categories, and loans.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Root endpoint
@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "Welcome to Library Management System API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Member endpoints
@app.post("/members/", response_model=schemas.Member, tags=["Members"])
def create_member(member: schemas.MemberCreate, db: Session = Depends(get_db)):
    """Create a new library member."""
    return crud.create_member(db=db, member=member)

@app.get("/members/", response_model=List[schemas.Member], tags=["Members"])
def read_members(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve all library members with pagination."""
    return crud.get_members(db, skip=skip, limit=limit)

@app.get("/members/{member_id}", response_model=schemas.Member, tags=["Members"])
def read_member(member_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific member by ID."""
    return crud.get_member(db, member_id=member_id)

@app.put("/members/{member_id}", response_model=schemas.Member, tags=["Members"])
def update_member(member_id: int, member_update: schemas.MemberUpdate, db: Session = Depends(get_db)):
    """Update a member's information."""
    return crud.update_member(db, member_id=member_id, member_update=member_update)

@app.delete("/members/{member_id}", tags=["Members"])
def delete_member(member_id: int, db: Session = Depends(get_db)):
    """Delete a member (only if no active loans)."""
    return crud.delete_member(db, member_id=member_id)

# Book endpoints
@app.post("/books/", response_model=schemas.Book, tags=["Books"])
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """Add a new book to the library."""
    return crud.create_book(db=db, book=book)

@app.get("/books/", response_model=List[schemas.Book], tags=["Books"])
def read_books(
    skip: int = 0, 
    limit: int = 100, 
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    db: Session = Depends(get_db)
):
    """Retrieve all books with optional category filtering and pagination."""
    return crud.get_books(db, skip=skip, limit=limit, category_id=category_id)

@app.get("/books/{book_id}", response_model=schemas.Book, tags=["Books"])
def read_book(book_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific book by ID."""
    return crud.get_book(db, book_id=book_id)

@app.put("/books/{book_id}", response_model=schemas.Book, tags=["Books"])
def update_book(book_id: int, book_update: schemas.BookUpdate, db: Session = Depends(get_db)):
    """Update book information."""
    return crud.update_book(db, book_id=book_id, book_update=book_update)

@app.delete("/books/{book_id}", tags=["Books"])
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Delete a book (only if no active loans)."""
    return crud.delete_book(db, book_id=book_id)

# Category endpoints
@app.post("/categories/", response_model=schemas.Category, tags=["Categories"])
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    """Create a new book category."""
    return crud.create_category(db=db, category=category)

@app.get("/categories/", response_model=List[schemas.Category], tags=["Categories"])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve all categories with pagination."""
    return crud.get_categories(db, skip=skip, limit=limit)

@app.get("/categories/{category_id}", response_model=schemas.Category, tags=["Categories"])
def read_category(category_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific category by ID."""
    return crud.get_category(db, category_id=category_id)

# Loan endpoints
@app.post("/loans/", response_model=schemas.Loan, tags=["Loans"])
def create_loan(loan: schemas.LoanCreate, db: Session = Depends(get_db)):
    """Create a new book loan."""
    return crud.create_loan(db=db, loan=loan)

@app.get("/loans/", response_model=List[schemas.Loan], tags=["Loans"])
def read_loans(
    skip: int = 0, 
    limit: int = 100,
    member_id: Optional[int] = Query(None, description="Filter by member ID"),
    active_only: bool = Query(False, description="Show only active loans"),
    db: Session = Depends(get_db)
):
    """Retrieve loans with filtering options."""
    return crud.get_loans(db, skip=skip, limit=limit, member_id=member_id, active_only=active_only)

@app.put("/loans/{loan_id}/return", response_model=schemas.Loan, tags=["Loans"])
def return_book(loan_id: int, db: Session = Depends(get_db)):
    """Return a borrowed book."""
    return crud.return_book(db, loan_id=loan_id)

# Health check endpoint
@app.get("/health", tags=["Health"])
def health_check():
    """Check API health status."""
    return {"status": "healthy", "message": "API is running successfully"}

if __name__ == "__main__":
    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )