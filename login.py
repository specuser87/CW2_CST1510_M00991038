import bcrypt
import os

USER_DATA_FILE = "users.txt"

# --------
# Hashing Password
# --------

def hash_password(plain_text_password):
    password_bytes = plain_text_password.encode('utf-8')
    salt = bcrypt.gensalt(12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

# Verifying the password
def verify_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(
        plain_text_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )

# Check if the user exists
def user_exists(username):
    if not os.path.exists(USER_DATA_FILE):
        return False
    
    with open(USER_DATA_FILE, "r") as file:
        for line in file:
            if not line.strip() or "," not in line:
                continue  # skip empty or invalid lines
            stored_username, _ = line.strip().split(",", 1)
            if stored_username.strip() == username:
                return True
    return False

# Register a new user
def register_user(username, password):
    if user_exists(username):
        print(f"Error: Username '{username}' already exists.")
        return False
    
    hashed_pw = hash_password(password)
    
    # Remove extra spaces to avoid bcrypt errors
    with open(USER_DATA_FILE, "a") as file:
        file.write(f"{username},{hashed_pw}\n")
    
    print(f"Success: User '{username}' registered successfully!")
    return True

# Login user
def login_user(username, password):
    if not os.path.exists(USER_DATA_FILE):
        print("Error: No users registered yet.")
        return False
    
    with open(USER_DATA_FILE, "r") as file:
        for line in file:
            if not line.strip() or "," not in line:
                continue  # skip empty or invalid lines
            stored_username, stored_hash = line.strip().split(",", 1)
            stored_username = stored_username.strip()
            stored_hash = stored_hash.strip()
            
            if stored_username == username:
                try:
                    if verify_password(password, stored_hash):
                        print(f"Success: Welcome, {username}!")
                        return True
                    else:
                        print("Error: Invalid password.")
                        return False
                except ValueError:
                    print(f"Error: Stored password for {username} is invalid.")
                    return False
    
    print("Error: Username not found.")
    return False
