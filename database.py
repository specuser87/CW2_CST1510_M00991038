import sqlite3
import pandas as pd
import bcrypt
from datetime import datetime


class DatabaseManager:
    """Manages all database operations for the intelligence platform"""
    
    def __init__(self, db_path='DATA/intelligence_platform.db'):
        """Initialize database connection"""
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        print(f"✓ Connected to database: {db_path}")
    
    # ==================== TABLE CREATION ====================
    
    def create_all_tables(self):
        """Create all required tables for the platform"""
        
        # Users table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL
            )
        """)
        
        # Cyber incidents table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS cyber_incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                incident_id TEXT NOT NULL UNIQUE,
                threat_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                status TEXT NOT NULL,
                date_reported TEXT NOT NULL,
                date_resolved TEXT,
                assigned_analyst TEXT
            )
        """)
        
        # Datasets metadata table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS datasets_metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dataset_name TEXT NOT NULL UNIQUE,
                source_department TEXT NOT NULL,
                upload_date TEXT NOT NULL,
                file_size_mb REAL NOT NULL,
                row_count INTEGER NOT NULL,
                owner TEXT NOT NULL
            )
        """)
        
        # IT tickets table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS it_tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT NOT NULL UNIQUE,
                category TEXT NOT NULL,
                priority TEXT NOT NULL,
                status TEXT NOT NULL,
                assigned_staff TEXT NOT NULL,
                date_created TEXT NOT NULL,
                date_resolved TEXT,
                resolution_time_hours REAL
            )
        """)
        
        self.conn.commit()
        print("✓ All tables created successfully")
    
    # ==================== DATA MIGRATION ====================
    
    def migrate_users_from_txt(self, file_path='DATA/users.txt'):
        """Migrate users from Week 7 text file to database"""
        try:
            with open(file_path, 'r') as file:
                migrated_count = 0
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Parse the line (format: username,password_hash,role)
                    parts = line.split(',')
                    if len(parts) >= 3:
                        username = parts[0].strip()
                        password_hash = parts[1].strip()
                        role = parts[2].strip()
                        
                        try:
                            self.cursor.execute("""
                                INSERT INTO users (username, password_hash, role)
                                VALUES (?, ?, ?)
                            """, (username, password_hash, role))
                            migrated_count += 1
                        except sqlite3.IntegrityError:
                            print(f"  ⚠ User '{username}' already exists, skipping")
                
                self.conn.commit()
                print(f"✓ Migrated {migrated_count} users from {file_path}")
        except FileNotFoundError:
            print(f"⚠ {file_path} not found - skipping migration")
        except Exception as e:
            print(f"✗ Error during migration: {e}")
    
    def load_csv_data(self):
        """Load all CSV files into their respective tables"""
        
        # Load Cyber Incidents
        try:
            df = pd.read_csv('DATA/cyber_incidents.csv')
            # Clean column names
            df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
            
            # Map CSV columns to database columns
            column_mapping = {
                'timestamp': 'date_reported',
                'date': 'date_reported',
                'reported_date': 'date_reported',
                'resolved_date': 'date_resolved',
            }
            df.rename(columns=column_mapping, inplace=True)
            
            # Select only columns that exist in our table
            required_cols = ['incident_id', 'threat_type', 'severity', 'status', 
                           'date_reported', 'date_resolved', 'assigned_analyst']
            available_cols = [col for col in required_cols if col in df.columns]
            df_filtered = df[available_cols]
            
            df_filtered.to_sql('cyber_incidents', self.conn, if_exists='append', index=False)
            print(f"✓ Loaded {len(df_filtered)} rows from DATA/cyber_incidents.csv")
        except FileNotFoundError:
            print(f"⚠ DATA/cyber_incidents.csv not found - skipping")
        except Exception as e:
            print(f"⚠ Could not load cyber_incidents.csv: {e}")
            print(f"  Available columns: {list(pd.read_csv('DATA/cyber_incidents.csv').columns)}")
        
        # Load Datasets Metadata
        try:
            df = pd.read_csv('DATA/datasets_metadata.csv')
            df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
            
            # Map CSV columns to database columns
            column_mapping = {
                'dataset_id': 'dataset_name',
                'name': 'dataset_name',
                'department': 'source_department',
                'source': 'source_department',
                'date': 'upload_date',
                'size_mb': 'file_size_mb',
                'size': 'file_size_mb',
                'rows': 'row_count',
                'count': 'row_count',
            }
            df.rename(columns=column_mapping, inplace=True)
            
            required_cols = ['dataset_name', 'source_department', 'upload_date', 
                           'file_size_mb', 'row_count', 'owner']
            available_cols = [col for col in required_cols if col in df.columns]
            df_filtered = df[available_cols]
            
            df_filtered.to_sql('datasets_metadata', self.conn, if_exists='append', index=False)
            print(f"✓ Loaded {len(df_filtered)} rows from DATA/datasets_metadata.csv")
        except FileNotFoundError:
            print(f"⚠ DATA/datasets_metadata.csv not found - skipping")
        except Exception as e:
            print(f"⚠ Could not load datasets_metadata.csv: {e}")
            print(f"  Available columns: {list(pd.read_csv('DATA/datasets_metadata.csv').columns)}")
        
        # Load IT Tickets
        try:
            df = pd.read_csv('DATA/it_tickets.csv')
            df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
            
            # Map CSV columns to database columns
            column_mapping = {
                'id': 'ticket_id',
                'type': 'category',
                'created': 'date_created',
                'created_date': 'date_created',
                'resolved': 'date_resolved',
                'resolved_date': 'date_resolved',
                'staff': 'assigned_staff',
                'resolution_time': 'resolution_time_hours',
            }
            df.rename(columns=column_mapping, inplace=True)
            
            required_cols = ['ticket_id', 'category', 'priority', 'status', 
                           'assigned_staff', 'date_created', 'date_resolved', 
                           'resolution_time_hours']
            available_cols = [col for col in required_cols if col in df.columns]
            df_filtered = df[available_cols]
            
            df_filtered.to_sql('it_tickets', self.conn, if_exists='append', index=False)
            print(f"✓ Loaded {len(df_filtered)} rows from DATA/it_tickets.csv")
        except FileNotFoundError:
            print(f"⚠ DATA/it_tickets.csv not found - skipping")
        except Exception as e:
            print(f"⚠ Could not load it_tickets.csv: {e}")
            print(f"  Available columns: {list(pd.read_csv('DATA/it_tickets.csv').columns)}")
    
    # ==================== USER CRUD ====================
    
    def create_user(self, username, password, role='user'):
        """Create a new user with hashed password"""
        # Hash the password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        try:
            self.cursor.execute("""
                INSERT INTO users (username, password_hash, role)
                VALUES (?, ?, ?)
            """, (username, password_hash.decode('utf-8'), role))
            self.conn.commit()
            print(f"✓ User '{username}' created successfully")
            return True
        except sqlite3.IntegrityError:
            print(f"✗ Username '{username}' already exists")
            return False
    
    def get_all_users(self):
        """Read all users"""
        self.cursor.execute("SELECT id, username, role FROM users")
        return self.cursor.fetchall()
    
    def get_user_by_username(self, username):
        """Get specific user by username"""
        self.cursor.execute("""
            SELECT id, username, password_hash, role 
            FROM users 
            WHERE username = ?
        """, (username,))
        return self.cursor.fetchone()
    
    def verify_user_password(self, username, password):
        """Verify user login credentials"""
        user = self.get_user_by_username(username)
        if user:
            stored_hash = user[2].encode('utf-8')
            return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
        return False
    
    def update_user_role(self, username, new_role):
        """Update user's role"""
        self.cursor.execute("""
            UPDATE users SET role = ? WHERE username = ?
        """, (new_role, username))
        self.conn.commit()
        print(f"✓ Updated role for '{username}' to '{new_role}'")
    
    def delete_user(self, username):
        """Delete a user"""
        self.cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        self.conn.commit()
        print(f"✓ Deleted user '{username}'")
    
    # ==================== CYBER INCIDENTS CRUD ====================
    
    def create_incident(self, incident_id, threat_type, severity, status, 
                       date_reported, date_resolved=None, assigned_analyst=None):
        """Create a new cyber incident"""
        try:
            self.cursor.execute("""
                INSERT INTO cyber_incidents 
                (incident_id, threat_type, severity, status, date_reported, 
                 date_resolved, assigned_analyst)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (incident_id, threat_type, severity, status, date_reported, 
                  date_resolved, assigned_analyst))
            self.conn.commit()
            print(f"✓ Incident '{incident_id}' created")
            return True
        except sqlite3.IntegrityError:
            print(f"✗ Incident '{incident_id}' already exists")
            return False
    
    def get_all_incidents(self, status=None):
        """Get all incidents, optionally filtered by status"""
        if status:
            self.cursor.execute("""
                SELECT * FROM cyber_incidents WHERE status = ?
            """, (status,))
        else:
            self.cursor.execute("SELECT * FROM cyber_incidents")
        return self.cursor.fetchall()
    
    def get_incident_by_id(self, incident_id):
        """Get specific incident"""
        self.cursor.execute("""
            SELECT * FROM cyber_incidents WHERE incident_id = ?
        """, (incident_id,))
        return self.cursor.fetchone()
    
    def update_incident(self, incident_id, **kwargs):
        """Update incident fields dynamically"""
        if not kwargs:
            print("⚠ No fields to update")
            return
        
        set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        values = list(kwargs.values()) + [incident_id]
        
        self.cursor.execute(f"""
            UPDATE cyber_incidents SET {set_clause} WHERE incident_id = ?
        """, values)
        self.conn.commit()
        print(f"✓ Updated incident '{incident_id}'")
    
    def delete_incident(self, incident_id):
        """Delete an incident"""
        self.cursor.execute("""
            DELETE FROM cyber_incidents WHERE incident_id = ?
        """, (incident_id,))
        self.conn.commit()
        print(f"✓ Deleted incident '{incident_id}'")
    
    # ==================== DATASETS CRUD ====================
    
    def create_dataset(self, dataset_name, source_department, upload_date, 
                      file_size_mb, row_count, owner):
        """Create a new dataset record"""
        try:
            self.cursor.execute("""
                INSERT INTO datasets_metadata 
                (dataset_name, source_department, upload_date, file_size_mb, row_count, owner)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (dataset_name, source_department, upload_date, file_size_mb, row_count, owner))
            self.conn.commit()
            print(f"✓ Dataset '{dataset_name}' created")
            return True
        except sqlite3.IntegrityError:
            print(f"✗ Dataset '{dataset_name}' already exists")
            return False
    
    def get_all_datasets(self, source_department=None):
        """Get all datasets, optionally filtered by department"""
        if source_department:
            self.cursor.execute("""
                SELECT * FROM datasets_metadata WHERE source_department = ?
            """, (source_department,))
        else:
            self.cursor.execute("SELECT * FROM datasets_metadata")
        return self.cursor.fetchall()
    
    def get_dataset_by_name(self, dataset_name):
        """Get specific dataset"""
        self.cursor.execute("""
            SELECT * FROM datasets_metadata WHERE dataset_name = ?
        """, (dataset_name,))
        return self.cursor.fetchone()
    
    def update_dataset(self, dataset_name, **kwargs):
        """Update dataset fields dynamically"""
        if not kwargs:
            print("⚠ No fields to update")
            return
        
        set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        values = list(kwargs.values()) + [dataset_name]
        
        self.cursor.execute(f"""
            UPDATE datasets_metadata SET {set_clause} WHERE dataset_name = ?
        """, values)
        self.conn.commit()
        print(f"✓ Updated dataset '{dataset_name}'")
    
    def delete_dataset(self, dataset_name):
        """Delete a dataset"""
        self.cursor.execute("""
            DELETE FROM datasets_metadata WHERE dataset_name = ?
        """, (dataset_name,))
        self.conn.commit()
        print(f"✓ Deleted dataset '{dataset_name}'")
    
    # ==================== IT TICKETS CRUD ====================
    
    def create_ticket(self, ticket_id, category, priority, status, assigned_staff,
                     date_created, date_resolved=None, resolution_time_hours=None):
        """Create a new IT ticket"""
        try:
            self.cursor.execute("""
                INSERT INTO it_tickets 
                (ticket_id, category, priority, status, assigned_staff, date_created,
                 date_resolved, resolution_time_hours)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (ticket_id, category, priority, status, assigned_staff, date_created,
                  date_resolved, resolution_time_hours))
            self.conn.commit()
            print(f"✓ Ticket '{ticket_id}' created")
            return True
        except sqlite3.IntegrityError:
            print(f"✗ Ticket '{ticket_id}' already exists")
            return False
    
    def get_all_tickets(self, status=None):
        """Get all tickets, optionally filtered by status"""
        if status:
            self.cursor.execute("""
                SELECT * FROM it_tickets WHERE status = ?
            """, (status,))
        else:
            self.cursor.execute("SELECT * FROM it_tickets")
        return self.cursor.fetchall()
    
    def get_ticket_by_id(self, ticket_id):
        """Get specific ticket"""
        self.cursor.execute("""
            SELECT * FROM it_tickets WHERE ticket_id = ?
        """, (ticket_id,))
        return self.cursor.fetchone()
    
    def update_ticket(self, ticket_id, **kwargs):
        """Update ticket fields dynamically"""
        if not kwargs:
            print("⚠ No fields to update")
            return
        
        set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        values = list(kwargs.values()) + [ticket_id]
        
        self.cursor.execute(f"""
            UPDATE it_tickets SET {set_clause} WHERE ticket_id = ?
        """, values)
        self.conn.commit()
        print(f"✓ Updated ticket '{ticket_id}'")
    
    def delete_ticket(self, ticket_id):
        """Delete a ticket"""
        self.cursor.execute("""
            DELETE FROM it_tickets WHERE ticket_id = ?
        """, (ticket_id,))
        self.conn.commit()
        print(f"✓ Deleted ticket '{ticket_id}'")
    
    # ==================== UTILITY METHODS ====================
    
    def get_table_stats(self):
        """Get row counts for all tables"""
        tables = ['users', 'cyber_incidents', 'datasets_metadata', 'it_tickets']
        stats = {}
        for table in tables:
            self.cursor.execute(f"SELECT COUNT(*) FROM {table}")
            stats[table] = self.cursor.fetchone()[0]
        return stats
    
    def close(self):
        """Close database connection"""
        self.conn.close()
        print("✓ Database connection closed")


# ==================== MAIN TESTING SCRIPT ====================

if __name__ == "__main__":
    print("=" * 60)
    print("WEEK 8: DATABASE SETUP & CRUD DEMONSTRATION")
    print("=" * 60)
    
    # Initialize database
    db = DatabaseManager()
    
    # Step 1: Create all tables
    print("\n[STEP 1] Creating all tables...")
    db.create_all_tables()
    
    # Step 2: Migrate users from Week 7
    print("\n[STEP 2] Migrating users from users.txt...")
    db.migrate_users_from_txt()
    
    # Step 3: Load CSV data
    print("\n[STEP 3] Loading CSV data...")
    db.load_csv_data()
    
    # Step 4: Test User CRUD
    print("\n[STEP 4] Testing User CRUD Operations...")
    db.create_user('test_user', 'password123', 'analyst')
    
    # Verify login
    if db.verify_user_password('test_user', 'password123'):
        print("✓ Login verification successful")
    
    # Step 5: Test Incident CRUD
    print("\n[STEP 5] Testing Incident CRUD Operations...")
    db.create_incident('TEST-001', 'Phishing', 'High', 'Open', '2024-11-20', 
                      assigned_analyst='test_user')
    db.update_incident('TEST-001', status='Resolved', date_resolved='2024-11-21')
    
    # Step 6: Test Dataset CRUD
    print("\n[STEP 6] Testing Dataset CRUD Operations...")
    db.create_dataset('Test_Dataset', 'IT', '2024-11-20', 100.5, 5000, 'test_user')
    
    # Step 7: Test Ticket CRUD
    print("\n[STEP 7] Testing Ticket CRUD Operations...")
    db.create_ticket('TEST-TKT-001', 'Hardware', 'High', 'Open', 'test_user', '2024-11-20')
    
    # Final Stats
    print("\n[FINAL] Database Statistics:")
    print("-" * 60)
    stats = db.get_table_stats()
    for table, count in stats.items():
        print(f"  {table:25} : {count:5} rows")
    
    print("\n" + "=" * 60)
    print("✅ WEEK 8 COMPLETE! Database is ready for Week 9 (Streamlit)")
    print("=" * 60)
    
    # Close connection
    db.close()