import bcrypt
import os

USER_DATA_FILE = "users.txt"

#--------
# Hashing Password
#--------

def hash_password(plain_text_password):
    password_bytes = plain_text_password.encode('utf-8')
    salt = bcrypt.gensalt(12)
    hashed = bcrypt.hashpw(password_bytes, salt) 
    return hashed.decode('utf-8')
# Here is where the 8 bytes are now decoded and sent back into a string.
# Verifying the password
def verify_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(
        plain_text_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )

# We are encoding both password as we veriy the password by comparing them
#Now we are checking if the user exists.

def user_exists(username):
    if not os.path.exists(USER_DATA_FILE):
        return False
    
    with open (USER_DATA_FILE, "r") as file:
        for line in file:
            stored_username = line.strip().split(",")[0]
            if stored_username ==username:
                return True
    return False   

# Now we are registeting the user
def register_user(username, password):
    if user_exists(username):
        print(f"Error: Username '{username}' already exists.")
        return False
    
    hashed_pw = hash_password(password)

    with open (USER_DATA_FILE, "a") as file:
        file.write(f"{username}, {hashed_pw}\n")

    print(f"Success: User'{username}' registered successfully!")
    return True   

    # For this section is where we allow the user to then login.

def login_user(username, password):
    if not os.path.exists(USER_DATA_FILE):
        return False
    
    with open(USER_DATA_FILE, "r")as file:
        for line in file:
            stored_username, stored_hash = line.strip().split(",")
            if stored_username == username:
                if verify_password(password, stored_hash):
                    print(f"Success: Welcome, {username}!")
                    return True
                else:
                    print("Error: Invalid password.")
                    return False
    print("Error: Username not found.")
    return False  
# This is where the main menu would be (frontend)

def main():
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            username = input("Enter Username: ").strip()
            password = input("Enter password: ").strip()
            register_user(username, password)          

        elif choice == "2":
            username = input("Enter username: ").strip()
            password = input ("Enter password: ").strip() 
            login_user(username, password) 

        elif choice == "3":
            print("Exiting the program...")
            break

        else:
            print("Invalid choice. Try again.") 
if __name__ == "_main_":
    main()                   
         

      
