from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import os
from datetime import datetime

app = Flask(__name__, static_folder='.', static_url_path='')

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'signatures.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS signatures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT UNIQUE NOT NULL CHECK(role IN ('client', 'developer')),
            name TEXT NOT NULL,
            signature_data TEXT NOT NULL,
            signed_at TEXT NOT NULL,
            ip_address TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ===== Serve static files =====
@app.route('/')
def index():
    return send_from_directory('.', 'proposal.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

# ===== API: Get signatures =====
@app.route('/api/signatures', methods=['GET'])
def get_signatures():
    conn = get_db()
    rows = conn.execute('SELECT role, name, signature_data, signed_at FROM signatures').fetchall()
    conn.close()
    
    result = {
        'client': None,
        'developer': None
    }
    
    for row in rows:
        result[row['role']] = {
            'name': row['name'],
            'signature_data': row['signature_data'],
            'signed_at': row['signed_at']
        }
    
    return jsonify(result)

# ===== API: Save signature =====
@app.route('/api/signatures', methods=['POST'])
def save_signature():
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    role = data.get('role')
    name = data.get('name', '').strip()
    signature_data = data.get('signature_data', '')
    
    if role not in ('client', 'developer'):
        return jsonify({'error': 'Role harus "client" atau "developer"'}), 400
    
    if not name:
        return jsonify({'error': 'Nama tidak boleh kosong'}), 400
    
    if not signature_data:
        return jsonify({'error': 'Tanda tangan tidak boleh kosong'}), 400
    
    signed_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ip_address = request.remote_addr
    
    conn = get_db()
    conn.execute('''
        INSERT INTO signatures (role, name, signature_data, signed_at, ip_address)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(role) DO UPDATE SET
            name = excluded.name,
            signature_data = excluded.signature_data,
            signed_at = excluded.signed_at,
            ip_address = excluded.ip_address
    ''', (role, name, signature_data, signed_at, ip_address))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'signed_at': signed_at})

# ===== API: Reset signatures (admin) =====
@app.route('/api/signatures/reset', methods=['POST'])
def reset_signatures():
    conn = get_db()
    conn.execute('DELETE FROM signatures')
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Semua tanda tangan telah direset'})

if __name__ == '__main__':
    print('='*50)
    print('  PASARKU PROPOSAL SERVER')
    print("  Open: http://localhost:5000/proposal.html")
    print('='*50)
    app.run(host='0.0.0.0', port=5000, debug=True)
