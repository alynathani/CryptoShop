from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c21010889:Racing2424@csmysql.cs.cf.ac.uk:3306/c21010889_CryptoShop'
app.config['SECRET_KEY'] = '53bf2fb8e87ef114bd27e1c4'
db = SQLAlchemy(app) 
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

from CryptoShop import routes