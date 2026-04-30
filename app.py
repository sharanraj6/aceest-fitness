from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = "aceest_fitness.db"


PROGRAMS = {
    "Fat Loss": {"factor": 22},
    "Muscle Gain": {"factor": 35},
    "Beginner": {"factor": 26}
}

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            age INTEGER,
            weight REAL,
            program TEXT,
            calories INTEGER
        )
    """)
    conn.commit()
    conn.close()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "ACEest API is running"}), 200

@app.route('/client', methods=['POST'])
def add_client():
    data = request.json
    name = data.get('name')
    weight = data.get('weight')
    program = data.get('program')

    if not name or not program or program not in PROGRAMS:
        return jsonify({"error": "Invalid input data"}), 400

    calories = int(weight * PROGRAMS[program]["factor"]) if weight else 0

    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO clients (name, weight, program, calories) VALUES (?, ?, ?, ?)",
            (name, weight, program, calories)
        )
        conn.commit()
        conn.close()
        return jsonify({"message": f"Client {name} added successfully", "calories": calories}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Client already exists"}), 409

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)