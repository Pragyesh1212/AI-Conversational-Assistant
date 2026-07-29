from database.database import get_connection

conn = get_connection()

print("✅ Database Connected")

conn.close()