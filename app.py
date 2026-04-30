from flask import Flask, request, jsonify, render_template
import sqlite3
import os

app = Flask(__name__)
DB_NAME = "aceest_fitness.db"

PROGRAMS = {
    "Fat Loss (FL)": {"factor": 22},
    "Muscle Gain (MG)": {"factor": 35},
    "Beginner (BG)": {"factor": 26}
}

def init_db(db_path=DB_NAME):
    """Initialize the database with the clients table."""
    conn = sqlite3.connect(db_path)
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

# Initialize DB on startup
init_db()

@app.route('/')
def home():
    """Render the main UI and fetch existing clients."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT name, age, weight, program, calories FROM clients")
    clients = cur.fetchall()
    conn.close()
    return render_template('index.html', clients=clients, programs=PROGRAMS.keys())
  
@app.route('/add_client', methods=['POST'])
def add_client():
    """API endpoint to calculate calories and save client to DB."""
    data = request.get_json()
    
    if not data or 'name' not in data or 'weight' not in data or 'program' not in data:
        return jsonify({"error": "Missing required data"}), 400

    name = data['name']
    age = data.get('age', 0)
    weight = float(data['weight'])
    program = data['program']

    if program not in PROGRAMS:
        return jsonify({"error": "Invalid program selected"}), 400

    calories = int(weight * PROGRAMS[program]["factor"])
    
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("""
            INSERT OR REPLACE INTO clients (name, age, weight, program, calories)
            VALUES (?, ?, ?, ?, ?)
        """, (name, age, weight, program, calories))
        conn.commit()
        conn.close()
        
        return jsonify({"message": "Client saved successfully", "calories": calories}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Added for Kubernetes Liveness Probe
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    # Running on port 8080 for standard Docker/Kubernetes routing
    app.run(host='0.0.0.0', port=8080)