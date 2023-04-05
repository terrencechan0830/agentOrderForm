import pytz
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from flask import Flask
from src.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(25), unique = True, nullable = False)
    email = db.Column(db.String(100), unique = False, nullable = False)
    phone = db.Column(db.String(10), unique = False, nullable = False)
    password = db.Column(db.String(100), nullable = False)
    ordergroups = db.relationship("OrderGroup", backref = "agent", lazy = True)
    orders = db.relationship("Order", backref = "agent", lazy = True)

    def get_reset_token(self):
        s = Serializer(current_app.config["SECRET_KEY"])
        return s.dumps({"user_id": self.id})

    @staticmethod
    def verify_reset_token(token, expires_sec = 1800):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token, expires_sec)["user_id"]
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        # return f"User('{self.username}', '{self.email}', '{self.phone}')"
        return self.username
        
class OrderGroup(db.Model):
    __tablename__ = "ordergroup"
    id = db.Column(db.Integer, primary_key = True)
    order_date = db.Column(db.DateTime, nullable = False, default = pytz.timezone("Asia/Hong_Kong").localize(datetime.now()))
    confirm_flag = db.Column(db.Boolean, unique = False, nullable = False)
    paid_flag = db.Column(db.Boolean, unique = False, nullable = False)
    fulfill_flag = db.Column(db.Boolean, unique = False, nullable = False)
    send_on_behalf_flag = db.Column(db.Boolean, unique = False, nullable = True)
    customername = db.Column(db.String(100), unique = False, nullable = True)
    customeraddress = db.Column(db.String(100), unique = False, nullable = True)
    customerphoneno = db.Column(db.String(100), unique = False, nullable = True)
    status = db.Column(db.String(100), unique = False, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)

    def __repr__(self):
        return f"OrderGroup('{self.id}', '{self.order_date}', '{self.confirm_flag}', '{self.paid_flag}', '{self.fulfill_flag}', '{self.send_on_behalf_flag}', '{self.customername}', '{self.customerphoneno}', '{self.customeraddress}', '{self.status}')"

class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key = True)
    order_group_id = db.Column(db.Integer, unique = False, nullable = False)
    product = db.Column(db.String(100), unique = False, nullable = False)
    quantity = db.Column(db.Integer, unique = False, nullable = False)
    arrival_flag = db.Column(db.Boolean, unique = False, nullable = False)
    fulfill_flag = db.Column(db.Boolean, unique = False, nullable = False)
    status = db.Column(db.String(100), unique = False, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)

    def __repr__(self):
        return f"Order('{self.id}', '{self.order_group_id}', '{self.product}', '{self.quantity}', '{self.arrival_flag}', '{self.fulfill_flag}', '{self.status}')"

def get_user():
    # return db.session.query(User.username)
    return User.query.filter(User.username != "Admin").all()

# db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"
mail.init_app(app)
from src.users.routes import users
from src.orders.routes import orders
from src.main.routes import main
from src.errors.handlers import errors
app.register_blueprint(users)
app.register_blueprint(orders)
app.register_blueprint(main)
app.register_blueprint(errors)