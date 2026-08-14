import sqlite3
#temporary script to update the database with new columns. This should be run once and then deleted.
DB_PATH = "database/spare.db"

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

# Add Material Issue status
try:
    cursor.execute("""
        ALTER TABLE material_issues
        ADD COLUMN status VARCHAR(20)
        DEFAULT 'COMPLETED'
    """)
    print("Added: material_issues.status")
except sqlite3.OperationalError as e:
    print("status:", e)

# Add invoiced flag
try:
    cursor.execute("""
        ALTER TABLE material_issues
        ADD COLUMN invoiced BOOLEAN
        DEFAULT 0
    """)
    print("Added: material_issues.invoiced")
except sqlite3.OperationalError as e:
    print("invoiced:", e)

connection.commit()
connection.close()

print("Database update completed.")