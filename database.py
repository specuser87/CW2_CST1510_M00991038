import sqlite3

# Connect to database (create it if it doesn't exist)
conn = sqlite3.connect('DATA/intelligence_platform.db')

def create_user_table():
    """Create the users table"""
    curr = conn.cursor()  # Fixed: added () and correct variable name
    sql = """CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL
    )"""
    
    curr.execute(sql)
    conn.commit()
    print("✓ Users table created")


def add_user(conn, username, password_hash, role):
    """Add a new user to the database"""
    curr = conn.cursor()
    sql = """INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)"""
    params = (username, password_hash, role)  # Fixed: use actual parameters
    
    try:
        curr.execute(sql, params)
        conn.commit()
        print(f"✓ User '{username}' added successfully")
    except sqlite3.IntegrityError:
        print(f"✗ Error: Username '{username}' already exists")


def get_all_users(conn):
    """Retrieve all users from database"""
    curr = conn.cursor()
    sql = """SELECT * FROM users"""
    curr.execute(sql)
    users = curr.fetchall()
    return users


def get_user_by_username(conn, username):
    """Get a specific user by username"""
    curr = conn.cursor()
    sql = """SELECT * FROM users WHERE username = ?"""
    curr.execute(sql, (username,))
    user = curr.fetchone()
    return user


def update_user_password(conn, username, new_password_hash):
    """Update a user's password"""
    curr = conn.cursor()
    sql = """UPDATE users SET password_hash = ? WHERE username = ?"""
    curr.execute(sql, (new_password_hash, username))
    conn.commit()
    print(f"✓ Password updated for user '{username}'")


def delete_user(conn, username):
    """Delete a user from the database"""
    curr = conn.cursor()
    sql = """DELETE FROM users WHERE username = ?"""
    curr.execute(sql, (username,))
    conn.commit()
    print(f"✓ User '{username}' deleted")


# ==================== TESTING ====================

if __name__ == "__main__":
    print("=== Setting up database ===\n")
    
    # Create table
    create_user_table()
    
    # Add some test users
    print("\n--- Adding users ---")
    add_user(conn, 'alice', 'hashed_password_123', 'admin')
    add_user(conn, 'bob', 'hashed_password_456', 'analyst')
    add_user(conn, 'alice', 'duplicate_test', 'user')  # This should fail
    
    # Read all users
    print("\n--- All users in database ---")
    users = get_all_users(conn)
    for user in users:
        print(f"ID: {user[0]}, Username: {user[1]}, Hash: {user[2]}, Role: {user[3]}")
    
    # Get specific user
    print("\n--- Getting user 'alice' ---")
    alice = get_user_by_username(conn, 'alice')
    if alice:
        print(f"Found: {alice}")
    
    # Update user
    print("\n--- Updating password ---")
    update_user_password(conn, 'alice', 'new_hashed_password_999')
    
    # Delete user
    print("\n--- Deleting user 'bob' ---")
    delete_user(conn, 'bob')
    
    # Show final state
    print("\n--- Final user list ---")
    users = get_all_users(conn)
    for user in users:
        print(f"Username: {user[1]}, Role: {user[3]}")
    
    # Close connection
    conn.close()
    print("\n✓ Database connection closed")
     

