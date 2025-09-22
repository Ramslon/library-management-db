#!/usr/bin/env python3
"""
Library Management System API
Startup script for the FastAPI application
"""

import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_tables():
    """Create database tables if database is available"""
    try:
        from app.database import engine
        from app import models
        print("Creating database tables...")
        models.Base.metadata.create_all(bind=engine)
        print("✓ Database tables created successfully!")
        return True
    except Exception as e:
        print(f"⚠️  Warning: Could not create database tables: {e}")
        print("Make sure your database is running and configured correctly in .env file")
        return False

if __name__ == "__main__":
    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    print(f"Starting Library Management System API...")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Debug mode: {debug}")
    
    # Try to create tables
    db_ready = create_tables()
    
    if not db_ready:
        print("\n" + "="*50)
        print("DATABASE SETUP REQUIRED")
        print("="*50)
        print("1. Install and start MySQL server")
        print("2. Create a database named 'LibraryDB'")
        print("3. Update the .env file with your database credentials:")
        print("   DB_HOST=localhost")
        print("   DB_PORT=3306")
        print("   DB_USER=your_username")
        print("   DB_PASSWORD=your_password")
        print("   DB_NAME=LibraryDB")
        print("4. Restart the application")
        print("="*50)
        print("\nStarting API anyway (database endpoints will fail)...")
    
    print(f"\nAPI Documentation: http://{host}:{port}/docs")
    print(f"Health Check: http://{host}:{port}/health")
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )