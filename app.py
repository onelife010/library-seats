from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os

app = Flask(__name__)

SEAT_FILE = "seats.json"
RESET_PASSWORD = os.environ.get("RESET_PASSWORD", "admin123")  # Secure default


# Load seat data from JSON
def load_seats():
    if not os.path.exists(SEAT_FILE):
        return []
    try:
        with open(SEAT_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


# Save seat data to JSON
def save_seats(seats):
    with open(SEAT_FILE, "w") as f:
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
            save_seats(seats)
            return jsonify({'success': True}), 200
    return jsonify({'success': False, 'message': 'Seat not found'}), 404


@app.route('/free/<int:seat_id>', methods=['POST'])
def free(seat_id):
    seats = load_seats()
    for seat in seats:
        if seat['id'] == seat_id:
            seat['status'] = 'available'
            save_seats(seats)
            return jsonify({'success': True}), 200
    return jsonify({'success': False, 'message': 'Seat not found'}), 404


@app.route("/reset", methods=["POST"])
def reset():
    password = request.form.get("password")
    if password == RESET_PASSWORD:
        seats = [{"id": i, "status": "available"} for i in range(1, 61)]  # Reset 60 seats
        save_seats(seats)
        return redirect("/")
    else:
        return "Incorrect password", 403


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
