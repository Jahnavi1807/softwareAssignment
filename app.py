from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'art'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Initialize MySQL
mysql = MySQL(app)

# Define route for homepage
@app.route('/')
def index():
    return render_template('index.html')

# Define route for booking tickets
@app.route('/book_tickets', methods=['GET', 'POST'])
def book_tickets():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        num_tickets = request.form['num_tickets']
        event_id = request.form['event_id']

        # Insert booking into database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO bookings(name, email, num_tickets, event_id) VALUES(%s, %s, %s, %s)", (name, email, num_tickets, event_id))
        mysql.connection.commit()
        cur.close()

        flash('Booking successful!')
        return redirect(url_for('index'))

    # Get event details from database
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM events")
    events = cur.fetchall()
    cur.close()

    return render_template('book_tickets.html', events=events)

# Define route for ticket generation
@app.route('/generate_ticket/<int:booking_id>')
def generate_ticket(booking_id):
    # Get booking details from database
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM bookings WHERE id=%s", (booking_id,))
    booking = cur.fetchone()
    cur.close()

    # Get event details from database
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM events WHERE id=%s", (booking['event_id'],))
    event = cur.fetchone()
    cur.close()

    return render_template('ticket.html', booking=booking, event=event)

# Define test script for booking tickets
def test_book_tickets():
    with app.test_client() as client:
        response = client.post('/book_tickets', data={
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'num_tickets': 2,
            'event_id': 104
        }, follow_redirects=True)
        assert b'Booking successful!' in response.data



# Define test script for generating ticket
def test_generate_ticket():
    with app.test_client() as client:
        response = client.get('/generate_ticket/1')
        assert b'Ticket Details' in response.data

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
    test_book_tickets()

