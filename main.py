from login import register_user, login_user


# Main menu
def main():
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            username = input("Enter Username: ").strip()
            password = input("Enter Password: ").strip()
            register_user(username, password)
        elif choice == "2":
            username = input("Enter Username: ").strip()
            password = input("Enter Password: ").strip()
            login_user(username, password)
        elif choice == "3":
            print("Exiting the program...")
            break
        else:
            print("Invalid choice. Try again.")



import sqlite3

con = sqlite3.connect("DATA/telligence_platform.db")

curr = con.cursor()

sql = (""" CREATE TABLE IF NOT EXISTS users ( 
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE NOT NULL,
password_hash TEXT NOT NULL,
role TEXT DEFAULT 'user'
);
""")


curr.execute(sql)

con.commit()

con.close()



          
