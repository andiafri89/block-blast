"""Backend API untuk Block Blast - High Score via PostgreSQL."""
from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)  # Izinkan akses dari HTML lokal

DB_CONFIG = {
    "host": "localhost",
    "database": "game",
    "user": "postgres",
    "password": "0809",
    "port": "5432"
}


def get_db():
    """Buka koneksi database."""
    return psycopg2.connect(**DB_CONFIG)


@app.route("/api/score", methods=["GET"])
def get_best_score():
    """Ambil skor tertinggi."""
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT score FROM high_scores WHERE username = 'default'")
        row = cur.fetchone()
        cur.close()
        conn.close()
        score = row[0] if row else 0
        return jsonify({"success": True, "score": score})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/score", methods=["POST"])
def save_score():
    """Simpan skor baru jika lebih tinggi."""
    try:
        data = request.get_json()
        score = data.get("score", 0)

        conn = get_db()
        cur = conn.cursor()

        # Ambil skor saat ini
        cur.execute("SELECT score FROM high_scores WHERE username = 'default'")
        row = cur.fetchone()
        current_best = row[0] if row else 0

        is_new_best = False
        if score > current_best:
            cur.execute(
                "UPDATE high_scores SET score = %s, updated_at = CURRENT_TIMESTAMP WHERE username = 'default'",
                (score,)
            )
            conn.commit()
            is_new_best = True

        cur.close()
        conn.close()

        return jsonify({
            "success": True,
            "is_new_best": is_new_best,
            "best_score": max(score, current_best)
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    print("=== Block Blast API berjalan di http://localhost:5000 ===")
    app.run(host="0.0.0.0", port=5000, debug=True)
