from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class Profile(db.Model):
    email_id = db.Column(db.String(250), unique=True, nullable=False)
    username = db.Column(db.String(250), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(250), nullable=False)

    def __init__(self, email_id, username, password):
        self.email_id = email_id
        self.username = username
        self.password = password