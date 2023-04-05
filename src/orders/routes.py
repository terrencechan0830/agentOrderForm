from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from src.models import db, Order, OrderGroup, User
from src.orders.forms import OrderForm
from datetime import datetime
import pytz

orders = Blueprint("orders", __name__)

@orders.route("/order/new", methods = ["GET", "POST"])
@login_required
def new_order():
    form = OrderForm()

    if current_user.username == "Admin":
        if form.validate_on_submit():
            if request.method == 'POST':
                ordergroup = OrderGroup(order_date = pytz.timezone("Asia/Hong_Kong").localize(datetime.now()), send_on_behalf_flag = form.sendonbehalf.data,
                                        customername = form.customername.data, customerphoneno = form.customerphoneno.data, customeraddress = form.customeraddress.data,
                                        confirm_flag = False, paid_flag = False, fulfill_flag = False, status = "Processing", agent = form.agent.data)
                db.session.add(ordergroup)
                order_group_id = OrderGroup.query.order_by(OrderGroup.id.desc()).first().id
                num = len(request.form.getlist("product"))
                for i in range(num):
                    product = request.form.getlist("product")[i]
                    quantity = request.form.getlist("quantity")[i]
                    order = Order(order_group_id = order_group_id, product = product, quantity = quantity, arrival_flag = False, fulfill_flag = False, status = "Processing", agent = form.agent.data)
                    db.session.add(order)
                db.session.commit()
            flash("Your order has been created!", "success")
            return redirect(url_for("orders.new_order"))
        return render_template("admin_create_order.html", title = "New Order", form = form, legend = "Create Order")
    else:
        form.agent.data = current_user
        if form.validate_on_submit():
            if request.method == 'POST':
                ordergroup = OrderGroup(order_date = pytz.timezone("Asia/Hong_Kong").localize(datetime.now()), send_on_behalf_flag = form.sendonbehalf.data,
                                        customername = form.customername.data, customerphoneno = form.customerphoneno.data, customeraddress = form.customeraddress.data,
                                        confirm_flag = False, paid_flag = False, fulfill_flag = False, status = "Processing", agent = form.agent.data)
                db.session.add(ordergroup)
                order_group_id = OrderGroup.query.order_by(OrderGroup.id.desc()).first().id
                num = len(request.form.getlist("product"))
                for i in range(num):
                    product = request.form.getlist("product")[i]
                    quantity = request.form.getlist("quantity")[i]
                    order = Order(order_group_id = order_group_id, product = product, quantity = quantity, arrival_flag = False, fulfill_flag = False, status = "Processing", agent = form.agent.data)
                    db.session.add(order)
                db.session.commit()
            flash("Your order has been created!", "success")
            return redirect(url_for("orders.new_order"))
        return render_template("create_order.html", title = "New Order", form = form, legend = "Create Order")

    
@orders.route("/ordergroup/<int:order_group_id>/update", methods = ["GET", "POST"])
@login_required
def update_order_group(order_group_id):
    form = OrderForm()
    ordergroup = OrderGroup.query.get_or_404(order_group_id)
    form.agent.data = ordergroup.agent
    if ordergroup.agent != current_user and current_user.username != 'Admin':
        abort(403)
    if current_user.username == "Admin":
        if form.validate_on_submit():
            ordergroup.confirm_flag = False if len(request.form.getlist("confirm_check")) == 0 else True
            ordergroup.paid_flag = False if len(request.form.getlist("paid_check")) == 0 else True
            ordergroup.fulfill_flag = False if len(request.form.getlist("fulfill_check")) == 0 else True
            ordergroup.send_on_behalf_flag = form.sendonbehalf.data
            ordergroup.customername = form.customername.data if form.sendonbehalf.data else ""
            ordergroup.customerphoneno = form.customerphoneno.data if form.sendonbehalf.data else ""
            ordergroup.customeraddress = form.customeraddress.data if form.sendonbehalf.data else ""

            orders = Order.query.filter_by(order_group_id = order_group_id)
            num = len(request.form.getlist("product"))

            # Cancel previous orders
            for order in orders.all():
                order.status = "Cancelled"

            # Update new orders
            for i in range(num):
                product = request.form.getlist("product")[i]
                quantity = request.form.getlist("quantity")[i]
                arrival_flag = False if len(request.form.getlist("arrival_check" + str(i+1))) == 0 else True
                fulfill_flag = False if len(request.form.getlist("fulfill_check" + str(i+1))) == 0 else True
                order = Order(order_group_id = order_group_id, product = product, quantity = quantity, arrival_flag = arrival_flag, fulfill_flag = fulfill_flag, status = "Processing", agent = ordergroup.agent)
                db.session.add(order)
            db.session.commit()
            flash("Your order has been updated!", "success")
            return redirect(url_for("main.order_history"))
        elif request.method == "GET":
            orders = []
            for item in Order.query.filter_by(order_group_id = order_group_id).filter(Order.status != "Cancelled").all():
                dummy = {"product": "", "quantity": ""}
                dummy["product"] = item.product
                dummy["quantity"] = item.quantity
                dummy["arrival_flag"] = item.arrival_flag
                dummy["fulfill_flag"] = item.fulfill_flag
                orders.append(dummy)
        return render_template("admin_edit_order_group.html", title = "Admin Update Order", legend = "Admin Update Order", form = form, orders = orders, ordergroup = ordergroup, order_group_id = order_group_id)
    else:
        if form.validate_on_submit():
            ordergroup.send_on_behalf_flag = form.sendonbehalf.data
            ordergroup.customername = form.customername.data if form.sendonbehalf.data else ""
            ordergroup.customerphoneno = form.customerphoneno.data if form.sendonbehalf.data else ""
            ordergroup.customeraddress = form.customeraddress.data if form.sendonbehalf.data else ""

            orders = Order.query.filter_by(order_group_id = order_group_id)
            num = len(request.form.getlist("product"))

            # Cancel previous orders
            for order in orders.all():
                order.status = "Cancelled"

            # Update new orders
            for i in range(num):
                product = request.form.getlist("product")[i]
                quantity = request.form.getlist("quantity")[i]
                order = Order(order_group_id = order_group_id, product = product, quantity = quantity, arrival_flag = False, fulfill_flag = False, status = "Processing", agent = current_user)
                db.session.add(order)
            db.session.commit()
            
            flash("Your order has been updated!", "success")
            return redirect(url_for("main.order_history"))
        elif request.method == "GET":
            orders = []
            for item in Order.query.filter_by(order_group_id = order_group_id).filter(Order.status != "Cancelled").all():
                dummy = {"product": "", "quantity": ""}
                dummy["product"] = item.product
                dummy["quantity"] = item.quantity
                orders.append(dummy)
        return render_template("edit_order_group.html", title = "Update Order", legend = "Update Order", form = form, orders = orders, ordergroup = ordergroup, order_group_id = order_group_id)


@orders.route("/ordergroup/<int:order_group_id>/delete", methods = ["POST"])
@login_required
def delete_order_group(order_group_id):
    ordergroup = OrderGroup.query.get_or_404(order_group_id)
    if ordergroup.agent != current_user and current_user.username != 'Admin':
        abort(403)
    ordergroup.status = "Cancelled"
    ordergroup.send_on_behalf_flag = False
    orders = Order.query.filter_by(order_group_id = order_group_id)
    for order in orders:
        order.status = "Cancelled"
    db.session.commit()
    flash("Your order has been deleted!", "success")
    return redirect(url_for("main.order_history"))

# @orders.route("/order/<int:order_id>")
# def order(order_id):
#     order = Order.query.get_or_404(order_id)
#     return render_template("order.html", title = order.product, order = order)


# @orders.route("/order/<int:order_id>/update", methods = ["GET", "POST"])
# @login_required
# def update_order(order_id):
#     order = Order.query.get_or_404(order_id)
#     if order.agent != current_user:
#         abort(403)
#     form = OrderForm()
#     if form.validate_on_submit():
#         order.product = form.product.data
#         order.quantity = form.quantity.data
#         db.session.commit()
#         flash("Your order has been updated!", "success")
#         return redirect(url_for("orders.order", order_id = order.id))
#     elif request.method == "GET":
#         form.product.data = order.product
#         form.quantity.data = order.quantity
#     return render_template("create_order.html", title = "Update Order", form = form, legend = "Update Order")


# @orders.route("/order/<int:order_id>/delete", methods = ["POST"])
# @login_required
# def delete_order(order_id):
#     order = Order.query.get_or_404(order_id)
#     if order.agent != current_user:
#         abort(403)
#     db.session.delete(order)
#     db.session.commit()
#     flash("Your order has been deleted!", "success")
#     return redirect(url_for("main.order_history"))

