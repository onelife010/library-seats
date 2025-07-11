from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os

app = Flask(__name__)

# Load seat data from JSON
def load_seats():
    with open("seats.json", "r") as f:
        return json.load(f)

# Save seat data to JSON
def save_seats(seats):
    with open("seats.json", "w") as f:
        json.dump(seats, f, indent=2)

@app.route('/')
def index():
    seats = load_seats()
    return render_template('index.html', seats=seats)

@app.route('/checkin/<int:seat_id>', methods=['POST'])
def checkin(seat_id):
    seats = load_seats()
    for seat in seats:
        if seat['id'] == seat_id:
            seat['status'] = 'occupied'
            break
    save_seats(seats)
    return redirect(url_for('index'))

@app.route('/free/<int:seat_id>', methods=['POST'])
def free(seat_id):
    seats = load_seats()
    for seat in seats:
        if seat['id'] == seat_id:
            seat['status'] = 'available'
            break
    save_seats(seats)
    return redirect(url_for('index'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
