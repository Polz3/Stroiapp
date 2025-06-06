
import sqlite3

db_path = "test.db"  # Путь к файлу базы данных
conn = sqlite3.connect(db_path)
cur = conn.cursor()

tables = ["materials", "workers", "tools", "tool_transfers", "subgroups"]
for table in tables:
    try:
        cur.execute(f"UPDATE {table} SET user_id = 1 WHERE user_id IS NULL")
        print(f"✔ Updated {table}")
    except Exception as e:
        print(f"❌ Failed to update {table}: {e}")

conn.commit()
conn.close()
print("Готово. Все user_id = 1 обновлены.")
