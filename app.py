from flask import Flask, request, jsonify, redirect
import psycopg2
import os

app = Flask(__name__)

# Load Database URL from Railway
DATABASE_URL = os.getenv("DATABASE_URL")

# Connect to PostgreSQL Database
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# Create Tables (Runs Once)
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY,
            has_permission BOOLEAN DEFAULT FALSE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS links (
            short_link TEXT PRIMARY KEY,
            original_link TEXT
        )
    ''')

    conn.commit()
    cursor.close()
    conn.close()

init_db()

@app.route('/')
def home():
    return "Flask API is running on Railway! 🚀"

@app.route('/generate', methods=['POST'])
def generate_link():
    data = request.json
    original_link = data.get("invite_link")

    if not original_link:
        return jsonify({"error": "Missing invite_link"}), 400

    short_link = f"https://t.me/MyBot2?start={hash(original_link)}"

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO links (short_link, original_link) VALUES (%s, %s) ON CONFLICT (short_link) DO NOTHING", (short_link, original_link))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"miniapp_link": short_link})

if __name__ == "__main__":
    app.run(debug=True)
