import sqlite3

class DatabaseManager:
    def __init__(self, db_name="platform.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
    
    def create_tables(self):
        # Cybersecurity table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS cyber_incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                incident_type TEXT,
                severity TEXT,
                resolution_time INTEGER
            );
        """)

        # Data Science table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS datasets_metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dataset_name TEXT,
                size_mb REAL,
                department TEXT
            );
        """)

        # IT Table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS it_tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                staff_name TEXT,
                status TEXT,
                resolution_time INTEGER
            );
        """)

        self.connection.commit()
        print("Tables created successfully!")

    def close(self):
        self.cursor.close()
        self.connection.close()

if __name__=="__main__":
    db = DatabaseManager()
    db.create_tables()
    db.close()


