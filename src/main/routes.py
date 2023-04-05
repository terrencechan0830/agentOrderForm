from flask import Blueprint
from flask import render_template, request, Blueprint
from flask_login import current_user, login_required
from src.models import Order, OrderGroup

main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home")
def home():
    return render_template("home.html")

@main.route("/order_history")
@login_required
def order_history():
    page = request.args.get("page", 1, type = int)
    if current_user.username != 'Admin':
        ordergroups = OrderGroup.query.filter_by(user_id = current_user.id).order_by(OrderGroup.id.desc()).paginate(page=page, per_page=5)
        orders = Order.query.filter_by(user_id = current_user.id).filter(Order.status != "Cancelled").order_by(Order.order_group_id.desc()).order_by(Order.id)
        return render_template("order_history.html", orders = orders, ordergroups = ordergroups)
    else:
        ordergroups = OrderGroup.query.order_by(OrderGroup.id.desc()).paginate(page=page, per_page=5)
        orders = Order.query.filter(Order.status != "Cancelled").order_by(Order.order_group_id.desc()).order_by(Order.id)
        return render_template("admin_order_history.html", orders = orders, ordergroups = ordergroups)
    

@main.route("/guide")
def guide():
    return render_template("guide.html", title = "Guide")

@main.route("/testing", methods = ["GET", "POST"])
def testing():
    render_template("testing.html")