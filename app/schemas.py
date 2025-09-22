from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date

# Member Schemas
class MemberBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None

class MemberCreate(MemberBase):
    pass

class MemberUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

class Member(MemberBase):
    member_id: int
    join_date: date
    
    class Config:
        from_attributes = True

# Category Schemas
class CategoryBase(BaseModel):
    category_name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    category_id: int
    
    class Config:
        from_attributes = True

# Book Schemas
class BookBase(BaseModel):
    title: str
    isbn: str
    published_year: Optional[int] = None
    category_id: Optional[int] = None
    copies_available: int = 1

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    isbn: Optional[str] = None
    published_year: Optional[int] = None
    category_id: Optional[int] = None
    copies_available: Optional[int] = None

class Book(BookBase):
    book_id: int
    category: Optional[Category] = None
    
    class Config:
        from_attributes = True

# Author Schemas
class AuthorBase(BaseModel):
    first_name: str
    last_name: str

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    author_id: int
    
    class Config:
        from_attributes = True

# Loan Schemas
class LoanBase(BaseModel):
    member_id: int
    book_id: int
    due_date: date

class LoanCreate(LoanBase):
    pass

class LoanUpdate(BaseModel):
    due_date: Optional[date] = None
    return_date: Optional[date] = None

class Loan(LoanBase):
    loan_id: int
    loan_date: date
    return_date: Optional[date] = None
    member: Optional[Member] = None
    book: Optional[Book] = None
    
    class Config:
        from_attributes = True

# Response schemas
class MemberWithLoans(Member):
    loans: List[Loan] = []

class BookWithDetails(Book):
    loans: List[Loan] = []