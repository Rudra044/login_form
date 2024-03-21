from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Profile
from flask_bcrypt import Bcrypt 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
bcrypt = Bcrypt(app) 

@app.route('/register', methods=['POST'])
def add_user():
    data = request.json
    email_id = data.get('email_id')
    username = data.get('username')
    password = data.get('password')
    if email_id and username and password:
        if Profile.query.filter_by(email_id=email_id).first() or Profile.query.filter_by(username=username).first():
            return jsonify({'error': 'User with this email or username already exists'})
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = Profile(email_id=email_id, username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'})
    else:
        return jsonify({'error': 'Email, username, and password are required'})

@app.route('/login', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if username and password:
        user = Profile.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return jsonify({'message': 'Login successful'})
        else:
            return jsonify({'error': 'Invalid username or password'})
    else:
        return jsonify({'error': 'Username and password are required'})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
