from CryptoShop import app as application
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from CryptoShop.models import User, Currency, db
admin = Admin(application, name='Admin panel', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Currency, db.session))


if __name__ == '__main__':
    application.run(debug=True)