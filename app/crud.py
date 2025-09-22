from sqlalchemy.orm import Session
from sqlalchemy import and_
from app import models, schemas
from typing import List, Optional
from fastapi import HTTPException

# Member CRUD operations
def create_member(db: Session, member: schemas.MemberCreate):
    # Check if email already exists
    existing_member = db.query(models.Member).filter(models.Member.email == member.email).first()
    if existing_member:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_member = models.Member(**member.dict())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

def get_member(db: Session, member_id: int):
    member = db.query(models.Member).filter(models.Member.member_id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member

def get_members(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Member).offset(skip).limit(limit).all()

def get_member_by_email(db: Session, email: str):
    return db.query(models.Member).filter(models.Member.email == email).first()

def update_member(db: Session, member_id: int, member_update: schemas.MemberUpdate):
    db_member = get_member(db, member_id)
    
    # Check if email is being updated and if it already exists
    if member_update.email and member_update.email != db_member.email:
        existing_member = get_member_by_email(db, member_update.email)
        if existing_member:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    # Update only provided fields
    update_data = member_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_member, field, value)
    
    db.commit()
    db.refresh(db_member)
    return db_member

def delete_member(db: Session, member_id: int):
    db_member = get_member(db, member_id)
    
    # Check if member has active loans
    active_loans = db.query(models.Loan).filter(
        and_(models.Loan.member_id == member_id, models.Loan.return_date.is_(None))
    ).first()
    
    if active_loans:
        raise HTTPException(status_code=400, detail="Cannot delete member with active loans")
    
    db.delete(db_member)
    db.commit()
    return {"message": "Member deleted successfully"}

# Book CRUD operations
def create_book(db: Session, book: schemas.BookCreate):
    # Check if ISBN already exists
    existing_book = db.query(models.Book).filter(models.Book.isbn == book.isbn).first()
    if existing_book:
        raise HTTPException(status_code=400, detail="ISBN already exists")
    
    # Validate category exists if provided
    if book.category_id:
        category = db.query(models.Category).filter(models.Category.category_id == book.category_id).first()
        if not category:
            raise HTTPException(status_code=400, detail="Category not found")
    
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_book(db: Session, book_id: int):
    book = db.query(models.Book).filter(models.Book.book_id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

def get_books(db: Session, skip: int = 0, limit: int = 100, category_id: Optional[int] = None):
    query = db.query(models.Book)
    if category_id:
        query = query.filter(models.Book.category_id == category_id)
    return query.offset(skip).limit(limit).all()

def get_book_by_isbn(db: Session, isbn: str):
    return db.query(models.Book).filter(models.Book.isbn == isbn).first()

def update_book(db: Session, book_id: int, book_update: schemas.BookUpdate):
    db_book = get_book(db, book_id)
    
    # Check if ISBN is being updated and if it already exists
    if book_update.isbn and book_update.isbn != db_book.isbn:
        existing_book = get_book_by_isbn(db, book_update.isbn)
        if existing_book:
            raise HTTPException(status_code=400, detail="ISBN already exists")
    
    # Validate category exists if being updated
    if book_update.category_id:
        category = db.query(models.Category).filter(models.Category.category_id == book_update.category_id).first()
        if not category:
            raise HTTPException(status_code=400, detail="Category not found")
    
    # Update only provided fields
    update_data = book_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_book, field, value)
    
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    db_book = get_book(db, book_id)
    
    # Check if book has active loans
    active_loans = db.query(models.Loan).filter(
        and_(models.Loan.book_id == book_id, models.Loan.return_date.is_(None))
    ).first()
    
    if active_loans:
        raise HTTPException(status_code=400, detail="Cannot delete book with active loans")
    
    db.delete(db_book)
    db.commit()
    return {"message": "Book deleted successfully"}

# Category CRUD operations
def create_category(db: Session, category: schemas.CategoryCreate):
    # Check if category name already exists
    existing_category = db.query(models.Category).filter(models.Category.category_name == category.category_name).first()
    if existing_category:
        raise HTTPException(status_code=400, detail="Category name already exists")
    
    db_category = models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()

def get_category(db: Session, category_id: int):
    category = db.query(models.Category).filter(models.Category.category_id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

# Loan CRUD operations
def create_loan(db: Session, loan: schemas.LoanCreate):
    # Validate member exists
    member = get_member(db, loan.member_id)
    
    # Validate book exists and is available
    book = get_book(db, loan.book_id)
    if book.copies_available <= 0:
        raise HTTPException(status_code=400, detail="Book not available for loan")
    
    # Check if member already has this book on loan
    existing_loan = db.query(models.Loan).filter(
        and_(
            models.Loan.member_id == loan.member_id,
            models.Loan.book_id == loan.book_id,
            models.Loan.return_date.is_(None)
        )
    ).first()
    
    if existing_loan:
        raise HTTPException(status_code=400, detail="Member already has this book on loan")
    
    # Create loan and decrease available copies
    db_loan = models.Loan(**loan.dict())
    db.add(db_loan)
    book.copies_available -= 1
    
    db.commit()
    db.refresh(db_loan)
    return db_loan

def get_loans(db: Session, skip: int = 0, limit: int = 100, member_id: Optional[int] = None, active_only: bool = False):
    query = db.query(models.Loan)
    
    if member_id:
        query = query.filter(models.Loan.member_id == member_id)
    
    if active_only:
        query = query.filter(models.Loan.return_date.is_(None))
    
    return query.offset(skip).limit(limit).all()

def return_book(db: Session, loan_id: int):
    loan = db.query(models.Loan).filter(models.Loan.loan_id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    if loan.return_date:
        raise HTTPException(status_code=400, detail="Book already returned")
    
    # Set return date and increase available copies
    from datetime import date
    loan.return_date = date.today()
    
    book = get_book(db, loan.book_id)
    book.copies_available += 1
    
    db.commit()
    db.refresh(loan)
    return loan