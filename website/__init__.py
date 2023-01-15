from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_basicauth import BasicAuth

app = Flask(__name__)
basic_auth = BasicAuth(app)
app.config["SECRET_KEY"] = "343567c3"
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:nv7KXTnmcOVW7hbyj1XA@containers-us-west-18.railway.app:7994/railway"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from website import routes
