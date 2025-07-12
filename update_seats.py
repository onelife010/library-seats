

import sqlite3

# Connect to SQLite database (creates it if it doesn't exist)
conn = sqlite3.connect("seats.db")
c = conn.cursor()

# Create 'seats' table if it doesn't exist
c.execute('''
CREATE TABLE IF NOT EXISTS seats (
    id INTEGER PRIMARY KEY,
    status TEXT NOT NULL DEFAULT 'available'
)
''')

# Insert seats from 1 to 72 if not already present
for i in range(1, 73):
    c.execute("INSERT OR IGNORE INTO seats (id, status) VALUES (?, ?)", (i, 'available'))

# Save and close
conn.commit()
conn.close()

print("✅ Database initialized with 72 seats.")
