# Library Database Management System

A comprehensive library management system with SQL database schema and FastAPI CRUD application for managing books, members, authors, categories, and loan tracking.

## Project Components

This project includes:
1. **Database Schema** (`library_db.sql`) - Complete MySQL database structure
2. **FastAPI CRUD Application** - RESTful API for library management operations
3. **Comprehensive Documentation** - Setup instructions and API reference

## FastAPI CRUD Application

The FastAPI application provides a complete REST API for library management with the following features:

- **Member Management**: Create, read, update, and delete library members
- **Book Management**: Manage books with category relationships
- **Loan System**: Handle book borrowing and returns
- **Category Management**: Organize books by categories
- **Data Validation**: Pydantic schemas for request/response validation
- **Error Handling**: Comprehensive error responses
- **Interactive Documentation**: Auto-generated API docs with Swagger UI

### Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure database connection**:
   - Copy `.env` file and update database credentials
   - Ensure MySQL server is running
   - Database will be created automatically

3. **Run the application**:
   ```bash
   python run.py
   ```

4. **Access the API**:
   - API Documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc
   - API Base URL: http://localhost:8000

### API Endpoints

#### Members
- `POST /members/` - Create a new member
- `GET /members/` - Get all members (with pagination)
- `GET /members/{member_id}` - Get specific member
- `PUT /members/{member_id}` - Update member information
- `DELETE /members/{member_id}` - Delete member (if no active loans)

#### Books
- `POST /books/` - Add a new book
- `GET /books/` - Get all books (with optional category filtering)
- `GET /books/{book_id}` - Get specific book
- `PUT /books/{book_id}` - Update book information
- `DELETE /books/{book_id}` - Delete book (if no active loans)

#### Categories
- `POST /categories/` - Create a new category
- `GET /categories/` - Get all categories
- `GET /categories/{category_id}` - Get specific category

#### Loans
- `POST /loans/` - Create a new loan
- `GET /loans/` - Get loans (with filtering options)
- `PUT /loans/{loan_id}/return` - Return a borrowed book

### Example API Usage

#### Create a Member
```bash
curl -X POST "http://localhost:8000/members/" \
     -H "Content-Type: application/json" \
     -d '{
       "first_name": "John",
       "last_name": "Doe",
       "email": "john.doe@email.com",
       "phone": "555-0123"
     }'
```

#### Add a Book
```bash
curl -X POST "http://localhost:8000/books/" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "The Great Gatsby",
       "isbn": "978-0-7432-7356-5",
       "published_year": 1925,
       "category_id": 1,
       "copies_available": 3
     }'
```

#### Create a Loan
```bash
curl -X POST "http://localhost:8000/loans/" \
     -H "Content-Type: application/json" \
     -d '{
       "member_id": 1,
       "book_id": 1,
       "due_date": "2025-10-15"
     }'
```

## Database Schema Overview

This database system is designed to manage a library's core operations with the following main entities:

### Tables

#### 1. Members
Stores information about library members.
- `member_id` (Primary Key): Unique identifier for each member
- `first_name`: Member's first name
- `last_name`: Member's last name  
- `email`: Unique email address
- `phone`: Contact phone number
- `join_date`: Date when member joined the library

#### 2. Categories
Organizes books into different categories.
- `category_id` (Primary Key): Unique identifier for each category
- `category_name`: Name of the book category (e.g., Fiction, Science, History)

#### 3. Books
Contains information about all books in the library.
- `book_id` (Primary Key): Unique identifier for each book
- `title`: Book title
- `isbn`: International Standard Book Number (unique)
- `published_year`: Year the book was published
- `category_id` (Foreign Key): References Categories table
- `copies_available`: Number of copies available for loan

#### 4. Authors
Stores author information.
- `author_id` (Primary Key): Unique identifier for each author
- `first_name`: Author's first name
- `last_name`: Author's last name

#### 5. BookAuthors (Junction Table)
Handles the many-to-many relationship between books and authors.
- `book_id` (Foreign Key): References Books table
- `author_id` (Foreign Key): References Authors table
- Composite Primary Key: (book_id, author_id)

#### 6. Loans
Tracks book borrowing and returns.
- `loan_id` (Primary Key): Unique identifier for each loan
- `member_id` (Foreign Key): References Members table
- `book_id` (Foreign Key): References Books table
- `loan_date`: Date when book was borrowed
- `due_date`: Date when book should be returned
- `return_date`: Actual return date (NULL if not returned)

## Database Features

- **Referential Integrity**: Foreign key constraints ensure data consistency
- **Cascade Deletions**: Automatic cleanup of related records when books or authors are deleted
- **Default Values**: Automatic setting of join dates and loan dates
- **Unique Constraints**: Prevents duplicate emails, ISBNs, and category names
- **Many-to-Many Relationships**: Supports books with multiple authors

## Database Setup Instructions

### Prerequisites
- Python 3.8+ (including Python 3.13 with updated SQLAlchemy)
- MySQL 5.7+ or MariaDB 10.2+
- pip (Python package installer)

### Database Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/Ramslon/library-database-system.git
   cd library-database-system
   ```

2. **Set up Python environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure database connection**
   - Copy `.env.example` to `.env` (if provided) or create `.env` file:
   ```env
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_NAME=LibraryDB
   ```

4. **Create database manually** (if needed)
   ```bash
   mysql -u your_username -p
   CREATE DATABASE LibraryDB;
   ```

5. **Option 1: Use FastAPI (Recommended)**
   ```bash
   python run.py
   ```
   The application will automatically create tables when started.

6. **Option 2: Manual SQL execution**
   ```bash
   mysql -u your_username -p LibraryDB < library_db.sql
   ```

## Project Structure

```
library-database-system/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database connection
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   └── crud.py              # CRUD operations
├── library_db.sql           # Database schema
├── requirements.txt         # Python dependencies
├── .env                     # Environment configuration
├── run.py                   # Application startup script
└── README.md               # Documentation
```

## Testing the API

### Using the Interactive Documentation
1. Start the application: `python run.py`
2. Open http://localhost:8000/docs in your browser
3. Use the interactive interface to test endpoints

### Using curl
Test the health endpoint:
```bash
curl http://localhost:8000/health
```

### Using Python requests
```python
import requests

# Test connection
response = requests.get("http://localhost:8000/health")
print(response.json())

# Create a member
member_data = {
    "first_name": "Alice",
    "last_name": "Johnson",
    "email": "alice.johnson@email.com",
    "phone": "555-0124"
}
response = requests.post("http://localhost:8000/members/", json=member_data)
print(response.json())
```

## Usage Examples

### Sample Data Insertion

```sql
-- Add categories
INSERT INTO Categories (category_name) VALUES 
('Fiction'), ('Science'), ('History'), ('Technology');

-- Add authors
INSERT INTO Authors (first_name, last_name) VALUES 
('George', 'Orwell'), ('Isaac', 'Asimov'), ('Jane', 'Austen');

-- Add books
INSERT INTO Books (title, isbn, published_year, category_id, copies_available) VALUES 
('1984', '978-0-452-28423-4', 1949, 1, 3),
('Foundation', '978-0-553-29335-0', 1951, 2, 2),
('Pride and Prejudice', '978-0-14-143951-8', 1813, 1, 4);

-- Link books to authors
INSERT INTO BookAuthors (book_id, author_id) VALUES 
(1, 1), (2, 2), (3, 3);

-- Add members
INSERT INTO Members (first_name, last_name, email, phone) VALUES 
('John', 'Doe', 'john.doe@email.com', '555-0123'),
('Jane', 'Smith', 'jane.smith@email.com', '555-0124');

-- Record a loan
INSERT INTO Loans (member_id, book_id, due_date) VALUES 
(1, 1, DATE_ADD(CURRENT_DATE, INTERVAL 14 DAY));
```

### Common Queries

#### Find all books by a specific author
```sql
SELECT b.title, b.isbn, b.published_year 
FROM Books b
JOIN BookAuthors ba ON b.book_id = ba.book_id
JOIN Authors a ON ba.author_id = a.author_id
WHERE a.first_name = 'George' AND a.last_name = 'Orwell';
```

#### Check overdue books
```sql
SELECT m.first_name, m.last_name, b.title, l.due_date
FROM Loans l
JOIN Members m ON l.member_id = m.member_id
JOIN Books b ON l.book_id = b.book_id
WHERE l.return_date IS NULL AND l.due_date < CURRENT_DATE;
```

#### View available books by category
```sql
SELECT c.category_name, b.title, b.copies_available
FROM Books b
JOIN Categories c ON b.category_id = c.category_id
WHERE b.copies_available > 0
ORDER BY c.category_name, b.title;
```

## Database Relationships

```
Members (1) ----< (M) Loans (M) >---- (1) Books
                                              |
                                              | (M)
                                              |
                                              v
                                         Categories (1)
                                              
Books (M) ----< BookAuthors >---- (M) Authors
```

## Troubleshooting

### Python 3.13 Compatibility
If you encounter SQLAlchemy compatibility issues with Python 3.13:
- The latest version (SQLAlchemy 2.0.30+) in requirements.txt fixes this
- Run: `pip install -r requirements.txt` to update dependencies

### Database Connection Issues
If you see database connection errors:
1. Ensure MySQL server is running
2. Create the database: `CREATE DATABASE LibraryDB;`
3. Update `.env` file with correct credentials
4. The API will start even without database connection for testing

### Application Won't Start
- Check if port 8000 is available
- Try: `python run.py` instead of `uvicorn` directly
- Check the terminal output for specific error messages

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add some improvement'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Create a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Contact

For questions or suggestions, please open an issue or contact the repository owner.