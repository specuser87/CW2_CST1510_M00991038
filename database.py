import sqlite3
import pandas as pd

class DatabaseManager:
    """Handles all database operations for the Multi-Domain Intelligence Platform"""
    
    def __init__(self, db_name="intelligence_platform.db"):
        """Initialize database connection"""
        self.db_name = db_name
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        print(f"✓ Connected to database: {db_name}")
    
    def create_tables(self):
        """Create all required tables for the application"""
        
        # Users table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')
        
        # Cybersecurity incidents table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cyber_incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                incident_id TEXT UNIQUE,
                threat_type TEXT,
                severity TEXT,
                status TEXT,
                date_reported TEXT,
                date_resolved TEXT,
                assigned_analyst TEXT
            )
        ''')
        
        # Data Science datasets table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS datasets_metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dataset_name TEXT UNIQUE,
                source_department TEXT,
                upload_date TEXT,
                file_size_mb REAL,
                row_count INTEGER,
                owner TEXT
            )
        ''')
        
        # IT Operations tickets table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS it_tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT UNIQUE,
                category TEXT,
                priority TEXT,
                status TEXT,
                assigned_staff TEXT,
                date_created TEXT,
                date_resolved TEXT,
                resolution_time_hours REAL
            )
        ''')
        
        self.connection.commit()
        print("✓ All tables created successfully")
    
    def migrate_users_from_file(self, file_path="users.txt"):
        """Migrate user data from Week 7 text file to database"""
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    # Assuming format: username,password_hash,role
                    parts = line.strip().split(',')
                    if len(parts) == 3:
                        username, password_hash, role = parts
                        self.cursor.execute('''
                            INSERT OR IGNORE INTO users (username, password_hash, role)
                            VALUES (?, ?, ?)
                        ''', (username, password_hash, role))
            
            self.connection.commit()
            print("✓ Users migrated from file successfully")
        except FileNotFoundError:
            print("⚠ users.txt not found - skipping migration")
    
    # ==================== CRUD OPERATIONS FOR CYBER_INCIDENTS ====================
    
    def create_incident(self, incident_id, threat_type, severity, status, 
                       date_reported, date_resolved=None, assigned_analyst=None):
        """Create a new cybersecurity incident"""
        self.cursor.execute('''
            INSERT INTO cyber_incidents 
            (incident_id, threat_type, severity, status, date_reported, date_resolved, assigned_analyst)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (incident_id, threat_type, severity, status, date_reported, date_resolved, assigned_analyst))
        self.connection.commit()
        print(f"✓ Created incident: {incident_id}")
    
    def read_incidents(self, status=None):
        """Read all incidents or filter by status"""
        if status:
            self.cursor.execute('SELECT * FROM cyber_incidents WHERE status = ?', (status,))
        else:
            self.cursor.execute('SELECT * FROM cyber_incidents')
        return self.cursor.fetchall()
    
    def update_incident(self, incident_id, **kwargs):
        """Update an incident's fields"""
        # Build dynamic UPDATE query based on provided kwargs
        set_clause = ', '.join([f"{key} = ?" for key in kwargs.keys()])
        values = list(kwargs.values()) + [incident_id]
        
        query = f'UPDATE cyber_incidents SET {set_clause} WHERE incident_id = ?'
        self.cursor.execute(query, values)
        self.connection.commit()
        print(f"✓ Updated incident: {incident_id}")
    
    def delete_incident(self, incident_id):
        """Delete an incident"""
        self.cursor.execute('DELETE FROM cyber_incidents WHERE incident_id = ?', (incident_id,))
        self.connection.commit()
        print(f"✓ Deleted incident: {incident_id}")
    
    # ==================== CRUD OPERATIONS FOR DATASETS ====================
    
    def create_dataset(self, dataset_name, source_department, upload_date, 
                      file_size_mb, row_count, owner):
        """Create a new dataset record"""
        self.cursor.execute('''
            INSERT INTO datasets_metadata 
            (dataset_name, source_department, upload_date, file_size_mb, row_count, owner)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (dataset_name, source_department, upload_date, file_size_mb, row_count, owner))
        self.connection.commit()
        print(f"✓ Created dataset: {dataset_name}")
    
    def read_datasets(self, source_department=None):
        """Read all datasets or filter by department"""
        if source_department:
            self.cursor.execute('SELECT * FROM datasets_metadata WHERE source_department = ?', 
                              (source_department,))
        else:
            self.cursor.execute('SELECT * FROM datasets_metadata')
        return self.cursor.fetchall()
    
    def update_dataset(self, dataset_name, **kwargs):
        """Update a dataset's fields"""
        set_clause = ', '.join([f"{key} = ?" for key in kwargs.keys()])
        values = list(kwargs.values()) + [dataset_name]
        
        query = f'UPDATE datasets_metadata SET {set_clause} WHERE dataset_name = ?'
        self.cursor.execute(query, values)
        self.connection.commit()
        print(f"✓ Updated dataset: {dataset_name}")
    
    def delete_dataset(self, dataset_name):
        """Delete a dataset"""
        self.cursor.execute('DELETE FROM datasets_metadata WHERE dataset_name = ?', (dataset_name,))
        self.connection.commit()
        print(f"✓ Deleted dataset: {dataset_name}")
    
    # ==================== CRUD OPERATIONS FOR IT_TICKETS ====================
    
    def create_ticket(self, ticket_id, category, priority, status, assigned_staff,
                     date_created, date_resolved=None, resolution_time_hours=None):
        """Create a new IT ticket"""
        self.cursor.execute('''
            INSERT INTO it_tickets 
            (ticket_id, category, priority, status, assigned_staff, date_created, 
             date_resolved, resolution_time_hours)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (ticket_id, category, priority, status, assigned_staff, date_created, 
              date_resolved, resolution_time_hours))
        self.connection.commit()
        print(f"✓ Created ticket: {ticket_id}")
    
    def read_tickets(self, status=None):
        """Read all tickets or filter by status"""
        if status:
            self.cursor.execute('SELECT * FROM it_tickets WHERE status = ?', (status,))
        else:
            self.cursor.execute('SELECT * FROM it_tickets')
        return self.cursor.fetchall()
    
    def update_ticket(self, ticket_id, **kwargs):
        """Update a ticket's fields"""
        set_clause = ', '.join([f"{key} = ?" for key in kwargs.keys()])
        values = list(kwargs.values()) + [ticket_id]
        
        query = f'UPDATE it_tickets SET {set_clause} WHERE ticket_id = ?'
        self.cursor.execute(query, values)
        self.connection.commit()
        print(f"✓ Updated ticket: {ticket_id}")
    
    def delete_ticket(self, ticket_id):
        """Delete a ticket"""
        self.cursor.execute('DELETE FROM it_tickets WHERE ticket_id = ?', (ticket_id,))
        self.connection.commit()
        print(f"✓ Deleted ticket: {ticket_id}")
    
    # ==================== DATA LOADING FROM CSV ====================
    
    def load_csv_data(self, csv_file, table_name):
        """Load data from CSV file into specified table"""
        try:
            df = pd.read_csv(csv_file)
            df.to_sql(table_name, self.connection, if_exists='append', index=False)
            print(f"✓ Loaded {len(df)} rows from {csv_file} into {table_name}")
        except FileNotFoundError:
            print(f"⚠ {csv_file} not found - skipping")
        except Exception as e:
            print(f"✗ Error loading {csv_file}: {e}")
    
    def close(self):
        """Close database connection"""
        self.connection.close()
        print("✓ Database connection closed")


# ==================== TESTING/DEMO CODE ====================

if __name__ == "__main__":
    print("=== Week 8: Database Setup and CRUD Demo ===\n")
    
    # Initialize database
    db = DatabaseManager()
    
    # Create tables
    db.create_tables()
    
    # Migrate users from Week 7 (if file exists)
    db.migrate_users_from_file()
    
    # Demo: Create a test incident
    print("\n--- Testing CRUD Operations ---")
    db.create_incident(
        incident_id="INC-001",
        threat_type="Phishing",
        severity="High",
        status="Open",
        date_reported="2024-01-15",
        assigned_analyst="Alice"
    )
    
    # Read incidents
    print("\n--- All Incidents ---")
    incidents = db.read_incidents()
    for incident in incidents:
        print(incident)
    
    # Update incident
    db.update_incident("INC-001", status="Resolved", date_resolved="2024-01-16")
    
    # Load CSV data (if you have the files)
    print("\n--- Loading CSV Data ---")
    db.load_csv_data("cyber_incidents.csv", "cyber_incidents")
    db.load_csv_data("datasets_metadata.csv", "datasets_metadata")
    db.load_csv_data("it_tickets.csv", "it_tickets")
    
    # Close connection
    db.close()
    
    print("\n✓ Week 8 Complete! Database is ready to use.")