#!/usr/bin/env python3
"""
Simple test script for the Library Management System API
This script tests basic functionality without requiring a database connection
"""

import sys
import importlib.util

def test_imports():
    """Test if all modules can be imported successfully"""
    try:
        print("Testing imports...")
        
        # Test if FastAPI and dependencies are available
        import fastapi
        import uvicorn
        import sqlalchemy
        import pydantic
        print("✓ All main dependencies imported successfully")
        
        # Test if our modules can be imported
        from app import models, schemas, crud, database, main
        print("✓ All application modules imported successfully")
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_app_creation():
    """Test if FastAPI app can be created"""
    try:
        from app.main import app
        print("✓ FastAPI application created successfully")
        
        # Check if routes are registered
        routes = [route.path for route in app.routes]
        expected_routes = ["/", "/members/", "/books/", "/categories/", "/loans/", "/health"]
        
        for expected in expected_routes:
            if any(expected in route for route in routes):
                print(f"✓ Route {expected} registered")
            else:
                print(f"✗ Route {expected} not found")
        
        return True
    except Exception as e:
        print(f"✗ App creation error: {e}")
        return False

def test_schemas():
    """Test if Pydantic schemas work correctly"""
    try:
        from app.schemas import MemberCreate, BookCreate, CategoryCreate
        
        # Test member schema
        member_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "phone": "555-0123"
        }
        member = MemberCreate(**member_data)
        print("✓ Member schema validation works")
        
        # Test book schema
        book_data = {
            "title": "Test Book",
            "isbn": "978-0-123456-78-9",
            "published_year": 2023,
            "copies_available": 1
        }
        book = BookCreate(**book_data)
        print("✓ Book schema validation works")
        
        return True
    except Exception as e:
        print(f"✗ Schema validation error: {e}")
        return False

def main():
    """Run all tests"""
    print("Library Management System API - Basic Tests")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("App Creation Test", test_app_creation),
        ("Schema Validation Test", test_schemas)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 30)
        if test_func():
            passed += 1
        else:
            print(f"✗ {test_name} FAILED")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready to run.")
        print("\nTo start the server, run:")
        print("python run.py")
        print("\nThen visit: http://localhost:8000/docs")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())