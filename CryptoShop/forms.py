from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from CryptoShop.models import User

class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    username = StringField(label='Username:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Log In')

class AddToBasketForm(FlaskForm):
    submit = SubmitField(label='Add to Basket!')

class RemoveFromBasketForm(FlaskForm):
    submit = SubmitField(label='Remove from Basket!')

class AddToWishlistForm(FlaskForm):
    submit = SubmitField(label='Add to Wishlist!')

class RemoveFromWishlistForm(FlaskForm):
    submit = SubmitField(label='Remove from Wishlist!')

class CheckoutForm(FlaskForm):
    name_on_card = StringField(label='Name on Card:', validators=[Length(min=5, max=30), DataRequired()])
    card_number = StringField(label='Card Number:', validators=[Length(min=16, max=16), DataRequired()])
    card_month = StringField(label='Expiry Month:', validators=[Length(min=2, max=2), DataRequired()])
    card_year = StringField(label='Expiry Year:', validators=[Length(min=4, max=4), DataRequired()])
    CCV = StringField(label='CCV:', validators=[Length(min=2, max=4), DataRequired()])
    submit = SubmitField(label='Pay')
