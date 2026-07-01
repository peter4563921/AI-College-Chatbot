import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    port=int(os.getenv("MYSQL_PORT")),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE"),
    ssl_ca="ca.pem",
)

cursor = conn.cursor()

print("Connected to Aiven MySQL")

# Create Tables
with open("database/schema.sql", "r", encoding="utf-8") as f:
    sql = f.read()

for statement in sql.split(";"):
    statement = statement.strip()
    if statement:
        cursor.execute(statement)

conn.commit()

print("Schema created successfully")

# Insert Sample Data
with open("database/seed.sql", "r", encoding="utf-8") as f:
    sql = f.read()

for statement in sql.split(";"):
    statement = statement.strip()
    if statement:
        cursor.execute(statement)

conn.commit()

print("Seed data inserted successfully")

cursor.close()
conn.close()

print("Database setup completed.")