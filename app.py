from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# Load seats once into memory
SEATS_FILE = "seats.json"
seats_data = []

def load_seats():
    global seats_data
    with open(SEATS_FILE, "r") as f:
        seats_data = json.load(f)

def save_seats():
    with open(SEATS_FILE, "w") as f:
        json.dump(seats_data, f, indent=2)

# Load seats at app startup
load_seats()

@app.route("/")
def index():
    return render_template("index.html", seats=seats_data)

@app.route("/checkin/<int:seat_id>", methods=["POST"])
def checkin(seat_id):
    for seat in seats_data:
        if seat["id"] == seat_id:
            seat["status"] = "occupied"
            break
    save_seats()
    return redirect(url_for("index"))

@app.route("/free/<int:seat_id>", methods=["POST"])
def free(seat_id):
    for seat in seats_data:
        if seat["id"] == seat_id:
            seat["status"] = "available"
            break
    save_seats()
    return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
