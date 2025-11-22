from database import DatabaseManager


def display_menu():
    """Display main menu"""
    print("\n" + "="*50)
    print("MULTI-DOMAIN INTELLIGENCE PLATFORM - WEEK 8")
    print("="*50)
    print("1. Setup Database (First time only)")
    print("2. Register New User")
    print("3. Login User")
    print("4. View All Users")
    print("5. View Database Statistics")
    print("6. Test CRUD Operations")
    print("7. Exit")
    print("="*50)


def setup_database(db):
    """Initialize database with all tables and data"""
    print("\n--- Setting Up Database ---")
    db.create_all_tables()
    db.migrate_users_from_txt()
    db.load_csv_data()
    print("\n✓ Database setup complete!")


def register_user(db):
    """Register a new user"""
    print("\n--- Register New User ---")
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    role = input("Enter role (user/analyst/admin): ").strip() or 'user'
    
    db.create_user(username, password, role)


def login_user(db):
    """Login existing user"""
    print("\n--- User Login ---")
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    
    if db.verify_user_password(username, password):
        user = db.get_user_by_username(username)
        print(f"\n✓ Login successful!")
        print(f"Welcome, {username}!")
        print(f"Role: {user[3]}")
        return user
    else:
        print("\n✗ Login failed. Invalid username or password.")
        return None


def view_all_users(db):
    """Display all users"""
    print("\n--- All Users ---")
    users = db.get_all_users()
    
    if not users:
        print("No users found.")
        return
    
    print(f"\n{'ID':<5} {'Username':<20} {'Role':<15}")
    print("-" * 40)
    for user in users:
        print(f"{user[0]:<5} {user[1]:<20} {user[2]:<15}")
    print(f"\nTotal users: {len(users)}")


def view_stats(db):
    """Display database statistics"""
    print("\n--- Database Statistics ---")
    stats = db.get_table_stats()
    
    print(f"\n{'Table':<30} {'Rows':<10}")
    print("-" * 40)
    for table, count in stats.items():
        print(f"{table:<30} {count:<10}")


def test_crud_operations(db):
    """Demonstrate CRUD operations on all domains"""
    print("\n--- Testing CRUD Operations ---")
    
    # Test Incidents
    print("\n1. Testing Cyber Incidents...")
    db.create_incident('TEST-INC-001', 'Phishing', 'High', 'Open', 
                      '2024-11-21', assigned_analyst='test_user')
    incidents = db.get_all_incidents()
    print(f"   Total incidents: {len(incidents)}")
    
    # Test Datasets
    print("\n2. Testing Datasets...")
    db.create_dataset('Test_Dataset_2024', 'IT', '2024-11-21', 
                     50.5, 1000, 'test_user')
    datasets = db.get_all_datasets()
    print(f"   Total datasets: {len(datasets)}")
    
    # Test Tickets
    print("\n3. Testing IT Tickets...")
    db.create_ticket('TEST-TKT-001', 'Hardware', 'High', 'Open', 
                    'test_user', '2024-11-21')
    tickets = db.get_all_tickets()
    print(f"   Total tickets: {len(tickets)}")
    
    print("\n✓ CRUD operations completed successfully!")


def main():
    """Main program loop"""
    # Initialize database connection
    db = DatabaseManager()
    
    first_run = True
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '1':
            setup_database(db)
            first_run = False
            
        elif choice == '2':
            if first_run:
                print("\n⚠ Please run 'Setup Database' first (Option 1)")
                continue
            register_user(db)
            
        elif choice == '3':
            if first_run:
                print("\n⚠ Please run 'Setup Database' first (Option 1)")
                continue
            user = login_user(db)
            
        elif choice == '4':
            if first_run:
                print("\n⚠ Please run 'Setup Database' first (Option 1)")
                continue
            view_all_users(db)
            
        elif choice == '5':
            if first_run:
                print("\n⚠ Please run 'Setup Database' first (Option 1)")
                continue
            view_stats(db)
            
        elif choice == '6':
            if first_run:
                print("\n⚠ Please run 'Setup Database' first (Option 1)")
                continue
            test_crud_operations(db)
            
        elif choice == '7':
            print("\n✓ Closing database connection...")
            db.close()
            print("Goodbye!")
            break
            
        else:
            print("\n✗ Invalid choice. Please enter 1-7.")


if __name__ == "__main__":
    main()