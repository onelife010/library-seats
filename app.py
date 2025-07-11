from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

# In-memory seat data (resets every time the app restarts)
seats = [{"id": i + 1, "status": "available"} for i in range(60)]

@app.route('/')
def index():
    return render_template('index.html', seats=seats)

@app.route('/checkin/<int:seat_id>', methods=['POST'])
def checkin(seat_id):
    for seat in seats:
        if seat['id'] == seat_id:
            seat['status'] = 'occupied'
            break
    return redirect(url_for('index'))

@app.route('/free/<int:seat_id>', methods=['POST'])
def free(seat_id):
    for seat in seats:
        if seat['id'] == seat_id:
            seat['status'] = 'available'
            break
    return redirect(url_for('index'))

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
