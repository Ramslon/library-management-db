from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text, SmallInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Member(Base):
    __tablename__ = "Members"
    
    member_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(15))
    join_date = Column(Date, nullable=False, default=func.current_date())
    
    # Relationship with loans
    loans = relationship("Loan", back_populates="member")

class Category(Base):
    __tablename__ = "Categories"
    
    category_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category_name = Column(String(100), unique=True, nullable=False)
    
    # Relationship with books
    books = relationship("Book", back_populates="category")

class Book(Base):
    __tablename__ = "Books"
    
    book_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    isbn = Column(String(20), unique=True, nullable=False, index=True)
    published_year = Column(SmallInteger)
    category_id = Column(Integer, ForeignKey("Categories.category_id"))
    copies_available = Column(Integer, default=1)
    
    # Relationships
    category = relationship("Category", back_populates="books")
    book_authors = relationship("BookAuthor", back_populates="book")
    loans = relationship("Loan", back_populates="book")

class Author(Base):
    __tablename__ = "Authors"
    
    author_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    
    # Relationship with book_authors
    book_authors = relationship("BookAuthor", back_populates="author")

class BookAuthor(Base):
    __tablename__ = "BookAuthors"
    
    book_id = Column(Integer, ForeignKey("Books.book_id", ondelete="CASCADE"), primary_key=True)
    author_id = Column(Integer, ForeignKey("Authors.author_id", ondelete="CASCADE"), primary_key=True)
    
    # Relationships
    book = relationship("Book", back_populates="book_authors")
    author = relationship("Author", back_populates="book_authors")

class Loan(Base):
    __tablename__ = "Loans"
    
    loan_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey("Members.member_id"), nullable=False)
    book_id = Column(Integer, ForeignKey("Books.book_id"), nullable=False)
    loan_date = Column(Date, nullable=False, default=func.current_date())
    due_date = Column(Date, nullable=False)
    return_date = Column(Date)
    
    # Relationships
    member = relationship("Member", back_populates="loans")
    book = relationship("Book", back_populates="loans")