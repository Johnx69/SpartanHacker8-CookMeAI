from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from datetime import date
from app import db
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique = True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # Password
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')

    @password.setter
    def password(self, password):
        password_hash = generate_password_hash(password)

    def verify(self, password):
        return check_password_hash(self.password_hash, password)
    # Create a representation

    def __repr__(self):
        return '<Name %r>' % self.name


# Create a Blog Post model
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text())
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))