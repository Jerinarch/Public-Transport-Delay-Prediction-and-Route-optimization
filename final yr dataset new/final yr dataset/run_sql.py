import sqlite3
import pandas as pd
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

# Connect to database
db_path = 'bmtc_data_warehouse.db'
if not os.path.exists(db_path):
    print(f"Error: Database not found at {db_path}")
    sys.exit(1)
    
conn = sqlite3.connect(db_path)

# Read the SQL query from view1.sql
with open('view1.sql', 'r') as file:
    query = file.read()

print("Executing Query from view1.sql...\n")
print("-" * 80)
# Execute and format beautifully using Pandas
df = pd.read_sql_query(query, conn)
print(df.to_string(index=False))
print("-" * 80)

conn.close()
