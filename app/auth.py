from flask import Blueprint, request, redirect, url_for
from werkzeug.security import generate_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    password = request.form.get('password')
    hashed_pw = generate_password_hash(password, method='sha256')

    new_user = User(username=username, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    return 'User created successfully!'
