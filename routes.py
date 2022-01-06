from CryptoShop import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages, request
from CryptoShop.models import Currency, User
from CryptoShop.forms import RegisterForm, LoginForm, AddToBasketForm, RemoveFromBasketForm, AddToWishlistForm, RemoveFromWishlistForm, CheckoutForm
from CryptoShop import db
from flask_login import login_user, logout_user, login_required, current_user



@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/gallery', methods=['GET', 'POST'])
@login_required
def gallery_page():
    basket_form = AddToBasketForm()
    wishlist_form = AddToWishlistForm()
    if request.method == "POST":
        item_inbasket = request.form.get('item_inbasket')
        item_inwishlist = request.form.get('item_inwishlist')
        b_item_object = Currency.query.filter_by(name=item_inbasket).first()
        w_item_object = Currency.query.filter_by(name=item_inwishlist).first()
        if b_item_object:
            b_item_object.basketed = current_user.id
            current_user.total_spent += b_item_object.price
            db.session.commit()
            flash(f"You have added 1 {b_item_object.name} to your basket!", category='success')
        if w_item_object:
            w_item_object.wishlisted = current_user.id
            db.session.commit()
            flash(f"You have added 1 {w_item_object.name} to your wishlist!", category='success')
    
    



    if basket_form.validate_on_submit():
        print(request.form.get('item_inbasket'))
    
    items = Currency.query.all()



    return render_template('gallery.html', items=items, basket_form=basket_form, wishlist_form=wishlist_form)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()

    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, email_address=form.email_address.data, password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfull! You are now logged in as {user_to_create.username}", category='success')


        return redirect(url_for('gallery_page'))
    
    if form.errors != {}: #If there are no errors from validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET',  'POST'])

def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as {attempted_user.username}', category='success')
            return redirect(url_for('gallery_page'))
        else:
            flash('Username and password are not matching! Please try again', category='danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))

@app.route('/wishlist', methods=['GET', 'POST'])
@login_required
def wishlist_page():
    remove_wishlist_form = RemoveFromWishlistForm()
    if request.method == "POST":
        wishlist_removed = request.form.get('wishlist_removed')
        r_item_object = Currency.query.filter_by(name=wishlist_removed).first()
        if r_item_object:
            r_item_object.wishlisted = None
            db.session.commit()
            flash(f"You have removed 1 {r_item_object.name} from your wishlist!", category='success')
    items_in_wishlist = Currency.query.filter_by(wishlisted=current_user.id)
    return render_template('wishlist.html', items_in_wishlist=items_in_wishlist, remove_wishlist_form=remove_wishlist_form)

@app.route('/basket', methods=['GET', 'POST'])
@login_required
def basket_page():
    items_required = Currency.query.filter_by(basketed=current_user.id)
    total_number = 0

    for item in items_required:
        total_number += item.price
        current_user.total_spent = total_number
        db.session.commit()

    remove_form = RemoveFromBasketForm()
    if request.method == "POST":
        item_removed = request.form.get('item_removed')
        r_item_object = Currency.query.filter_by(name=item_removed).first()
        if r_item_object:
            r_item_object.basketed = None
            total_number -= r_item_object.price
            current_user.total_spent = total_number
            db.session.commit()
            flash(f"You have removed 1 {r_item_object.name} from your basket!", category='success')

    items_in_basket = Currency.query.filter_by(basketed=current_user.id)
    print(items_in_basket)
    return render_template('basket.html', items_in_basket=items_in_basket, remove_form=remove_form, total_number=total_number)

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout_page():
    form = CheckoutForm()

    if form.validate_on_submit():
        flash(f"You have successfully paid for these cryptocurrencies!", category='success')
    
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with your payment information: {err_msg}', category='danger')

    return render_template('checkout.html', form=form)

