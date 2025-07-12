from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
PASSWORD = "yourpassword"  # Set your reset password here

DB_PATH = 'seats.db'


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS seats (
            id INTEGER PRIMARY KEY,
            status TEXT NOT NULL
        )
    ''')
    # Insert seats if table is empty
    c.execute('SELECT COUNT(*) FROM seats')
    if c.fetchone()[0] == 0:
        for i in range(1, 61):
            c.execute('INSERT INTO seats (id, status) VALUES (?, ?)', (i, 'available'))
    conn.commit()
    conn.close()


def get_seats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, status FROM seats')
    seats = [{'id': row[0], 'status': row[1]} for row in c.fetchall()]
    conn.close()
    return seats


def update_seat(seat_id, status):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('UPDATE seats SET status = ? WHERE id = ?', (status, seat_id))
    conn.commit()
    conn.close()


def reset_all_seats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('UPDATE seats SET status = "available"')
    conn.commit()
    conn.close()


@app.route('/')
def index():
    seats = get_seats()
    return render_template('index.html', seats=seats)


@app.route('/checkin/<int:seat_id>', methods=['POST'])
def checkin(seat_id):
    update_seat(seat_id, 'occupied')
    return ('', 204)


@app.route('/free/<int:seat_id>', methods=['POST'])
def free(seat_id):
    update_seat(seat_id, 'available')
    return ('', 204)


@app.route('/reset', methods=['POST'])
def reset():
    password = request.form.get('password')
    if password == PASSWORD:
        reset_all_seats()
        return redirect(url_for('index'))
    else:
        return "Unauthorized", 403


if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
