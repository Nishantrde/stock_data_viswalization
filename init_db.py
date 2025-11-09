import sqlite3
import csv
import json

# Connect to the database (it will be created if not exists)
connection = sqlite3.connect('database.db')

# Run the schema file (create tables, etc.)
with open('schema.sql') as f:
    connection.executescript(f.read())

# Read the CSV file and convert it to a list of dicts
csv_file = "20251027_NSE.csv"
with open(csv_file, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)  # Convert to a list of dictionaries

# Convert the data to a JSON string
data_json = json.dumps(rows, indent=2)

# Insert the JSON string into the posts table
cur = connection.cursor()
cur.execute(
    "INSERT INTO posts (title, content) VALUES (?, ?)",
    ("NSE Data", data_json)
)

# Commit and close
connection.commit()
connection.close()

print("✅ CSV data successfully stored in the database as JSON!")
