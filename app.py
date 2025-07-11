from flask import Flask, render_template, request, jsonify
import json

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

@app.route('/update_seat', methods=['POST'])
def update_seat():
    data = request.json
    seat_id = data['seat_id']
    status = data['status']

    seats = load_seats()
    for seat in seats:
        if seat['id'] == seat_id:
            seat['status'] = status
            break
    save_seats(seats)
    return jsonify({'success': True})

if __name__ == "__main__":
    # Use 0.0.0.0 so it can be accessed externally (required for deployment)
    app.run(host="0.0.0.0", port=5000)
