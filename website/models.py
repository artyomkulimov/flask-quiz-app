from website import db
from werkzeug.security import generate_password_hash, check_password_hash
from website import db, login_manager
from flask_login import UserMixin

# creates tables in the database


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(500), nullable=False)
    marks = db.Column(db.Integer, index=True, default=0, nullable=False)
    top = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)


class Questions(db.Model):
    q_id = db.Column(db.Integer, primary_key=True)
    ques = db.Column(db.String(350), unique=True)
    a = db.Column(db.String(100))
    b = db.Column(db.String(100))
    c = db.Column(db.String(100))
    d = db.Column(db.String(100))
    ans = db.Column(db.String(100))

    def __repr__(self):
        return "<Question: {}>".format(self.ques)
