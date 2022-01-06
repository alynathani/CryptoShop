from CryptoShop import db, login_manager
from CryptoShop import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30),nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    currency_wishlist = db.relationship('Currency', backref='user_wishlisted', lazy=True)
    total_spent = db.Column(db.Integer(), nullable=False, default=0)

    @property
    def total_spent_number(self):
        return f"£{self.total_spent}"

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)





class Currency(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    image_name = db.Column(db.String(length=30), nullable=False, unique=True)
    symbol = db.Column(db.String(length=3), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    basketed = db.Column(db.Integer(), db.ForeignKey('user.id'))
    wishlisted = db.Column(db.Integer())

    def __repr__(self):
        return f'Currency {self.name}'