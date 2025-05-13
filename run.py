from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, login_user, logout_user,
    login_required, current_user, UserMixin
)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Passenger model for Titanic data
class Passenger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    age = db.Column(db.Float)
    sex = db.Column(db.String(10))
    survived = db.Column(db.Integer)
    pclass = db.Column(db.Integer)

# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return "Username already taken!"
    hashed_pw = generate_password_hash(password)
    new_user = User(username=username, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    return "Signup successful!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return "Invalid credentials!"
        login_user(user)
        return redirect('/dashboard')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/dashboard')
@login_required
def dashboard():
    return f"""
    Welcome, {current_user.username}!<br>
    <a href='/data-dashboard'>View Titanic Data</a>
    """

@app.route('/data-dashboard')
@login_required
def data_dashboard():
    passengers = Passenger.query.limit(20).all()
    total_survived = Passenger.query.filter_by(survived=1).count()
    total_died = Passenger.query.filter_by(survived=0).count()
    pclass_counts = db.session.query(Passenger.pclass, db.func.count(Passenger.id)).group_by(Passenger.pclass).all()

    return render_template(
        'dashboard.html',
        passengers=passengers,
        total_survived=total_survived,
        total_died=total_died,
        pclass_counts=pclass_counts
    )

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
