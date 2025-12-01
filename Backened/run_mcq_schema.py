"""
Run MCQ Schema Update from Python
This script runs the schema_mcq_update.sql file using your existing database connection
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration (same as App1.py)
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD'),
    'database': os.environ.get('DB_NAME', 'autorevise_db')
}

def run_sql_file(filename):
    """Execute SQL commands from a file"""
    try:
        # Read SQL file
        with open(filename, 'r') as file:
            sql_script = file.read()
        
        # Split into individual statements
        statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip()]
        
        # Connect to database
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print(f"Connected to database: {DB_CONFIG['database']}")
        print(f"Executing {len(statements)} SQL statements...\n")
        
        # Execute each statement
        for i, statement in enumerate(statements, 1):
            if statement.upper().startswith('SELECT') or statement.upper().startswith('SHOW'):
                # For SELECT/SHOW statements, fetch and display results
                cursor.execute(statement)
                results = cursor.fetchall()
                print(f"Statement {i}: {statement[:50]}...")
                for row in results:
                    print(f"  {row}")
            else:
                # For other statements (CREATE, ALTER, INSERT, UPDATE)
                cursor.execute(statement)
                print(f"✅ Statement {i} executed: {statement[:60]}...")
        
        # Commit changes
        connection.commit()
        print(f"\n✅ Successfully executed all statements!")
        print(f"✅ MCQ tables created successfully!")
        
    except Error as e:
        print(f"❌ Database error: {e}")
        return False
    
    except FileNotFoundError:
        print(f"❌ File not found: {filename}")
        return False
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("\n📊 Database connection closed.")
    
    return True

if __name__ == '__main__':
    print("=" * 60)
    print("MCQ Schema Update Script")
    print("=" * 60)
    
    # Run the schema update
    success = run_sql_file('schema_mcq_update.sql')
    
    if success:
        print("\n" + "=" * 60)
        print("Next step: Make a user admin")
        print("=" * 60)
        print("Run this in Python or MySQL:")
        print("  UPDATE Users SET is_admin = TRUE WHERE user_id = 1;")
        print("\nOr run the make_admin.py script.")
