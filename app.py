# app.py
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    with app.app_context():
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100))
        phone = db.Column(db.Integer)
        email = db.Column(db.String(100), unique=True)
        password = db.Column(db.String(100))
        address = db.Column(db.String(255))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']
        
        # Check if the email already exists in the database
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return "User with this email already exists!"
        
        with app.app_context():

            # Create a new User object and add it to the database session
            new_user = User(name=name, phone=phone, email=email, password=password, address=address)
            db.session.add(new_user)
            db.session.commit()

            
        return redirect(url_for(login))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            # You can add session management here to track logged-in users
            session['user_id'] = user.id
            return f"Login Successful! Welcome, {user.name}!"
        else:
            return "Invalid email or password. Please try again."
    return render_template('login.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin_password':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_view_users'))
        else:
            return "Invalid username or password. Please try again."
    return render_template('admin_login.html')

@app.route('/admin/view_users')
def admin_view_users():
    if 'admin_logged_in' in session:
        users = User.query.all()
        return render_template('admin_view_users.html', users=users)
    else: 
        return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug=True)
