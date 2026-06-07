"""Inisialisasi database untuk Block Blast high scores."""
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="game",
    user="postgres",
    password="0809",
    port="5432"
)
cur = conn.cursor()

# Buat tabel high_scores jika belum ada
cur.execute("""
    CREATE TABLE IF NOT EXISTS high_scores (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL DEFAULT 'default',
        score INTEGER NOT NULL DEFAULT 0,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""")

# Pastikan ada row default
cur.execute("""
    INSERT INTO high_scores (username, score)
    VALUES ('default', 0)
    ON CONFLICT (username) DO NOTHING;
""")

conn.commit()
cur.close()
conn.close()
print("Database berhasil diinisialisasi!")
