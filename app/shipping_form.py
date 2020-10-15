from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField, SelectField, BooleanField, SubmitField
)
from wtforms.validators import DataRequired
from map.map import map

class ShippingForm(FlaskForm):
    cities = [(k, k) for k in map.keys()]
    sender = StringField("Sender", [DataRequired()])
    recipient = StringField("Recipient", [DataRequired()])
    origin = SelectField("Origin", [DataRequired()], choices=cities)
    destination = SelectField("Destination", [DataRequired()], choices=cities)
    express = BooleanField("Express shipping")
    submit = SubmitField("Submit")