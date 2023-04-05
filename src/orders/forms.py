from xmlrpc.client import Boolean
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, TextAreaField, RadioField, BooleanField, FieldList, FormField, SelectField 
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField
from src.models import get_user

class OrderForm(FlaskForm):
    agent = QuerySelectField("Ordering Agent", validators = [DataRequired()], query_factory = get_user, allow_blank = True, blank_text = "-- Please select agent --")
    product = StringField("Product", validators = [DataRequired()])
    quantity = FloatField("Quantity", validators = [DataRequired()])
    sendonbehalf = BooleanField("SF Delivery?")
    arrival = BooleanField("Arrived?")
    fulfill = BooleanField("Fulfilled?")
    customername = StringField("Customer Name")
    customeraddress = StringField("Customer Address")
    customerphoneno = StringField("Customer Phone No.")
    submit = SubmitField('Submit')

class OrderEditForm(FlaskForm):
    orders = FieldList(FormField(OrderForm), min_entries = 2)
    submit = SubmitField('Submit')

