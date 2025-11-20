# CW2_CST1510_M00991038
This repository contains my coursework for CST1510.
README Summary for Week 7 – User Registration & Login System
Overview

This project implements a simple user authentication system in Python.
It allows users to:

Register with a username and password

Log in using previously saved credentials

Store user login data securely using bcrypt password hashing

Create a SQLite database table (for future use, even though Week 7 stores users in a text file)

The system is split into two main components:

main.py — Handles the user interface and sets up the database.

login.py — Handles password hashing, user registration, and login logic.

Explanation of Each File
1. main.py — Main Menu & Database Setup
What this file does

Displays a text-based menu with options: Register, Login, or Exit.

Interacts with functions from login.py (register_user and login_user).

Creates a SQLite users table (ID, username, hashed password, role) — though passwords for Week 7 are stored in a text file, this setup is preparing for Week 8 and beyond.

Key Features

Infinite loop until user chooses exit

Simple menu navigation

Inputs cleaned using .strip()

Database is created if it doesn’t already exist

Why the SQLite table is here

Even though Week 7 still stores users in a .txt file, this creates the database structure that will later replace the text-file storage method in Week 8/9.

2. login.py — User Authentication Logic
What this file does

This file manages everything related to user accounts:

✔ Password hashing using bcrypt
✔ Password verification
✔ Checking if a username already exists
✔ Writing user data to users.txt
✔ Validating user login attempts

Core Components
🔒 Password Hashing

Passwords are never stored in plain text.
hash_password() uses:

bcrypt.gensalt(12) → creates a strong salt

bcrypt.hashpw() → returns the hashed password

This ensures the system follows good security practices.

🔑 Login Verification

verify_password() checks whether the entered password matches the saved hashed password.

📄 User Storage

Users are saved in a text file:

username,hashed_password


This keeps Week 7 simple while still teaching secure password handling.

👤 Registration

register_user() checks:

If the username already exists

Hashes the password

Saves the new user to the file

🔐 Login

login_user():

Reads each stored user

Matches username

Verifies hashed password

Gives success or error messages

How the System Works Together
1. User launches the program

main() shows the menu.

2. User selects Register

main.py → login.py → hashes password → stores account

3. User selects Login

main.py → login.py → checks credentials → verifies password

4. Database table is created

Although not used yet, it ensures future compatibility for migrating from text-file storage to SQLite storage.

High-Level Summary

This Week 7 project demonstrates a secure, well-structured authentication system by:

Separating logic into two files (UI + authentication)

Using bcrypt hashing for strong password security

Maintaining simple storage through a text file

Preparing the system for future expansion using SQLite

