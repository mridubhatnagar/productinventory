from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, InputRequired, Length
from inventory.models import Product, Location

class ProductForm(FlaskForm):
    name=StringField('Name', validators=[DataRequired(), Length(min=2, max=200)])

class LocationForm(FlaskForm):
    name=StringField('Name', validators=[DataRequired(), Length(min=2, max=200)])

class ProductMovementForm(FlaskForm):
    from_location = SelectField('From Location ID', [DataRequired()], choices=[], 
        coerce=lambda x: x if x == ' ' else  int(x))
    to_location = SelectField('To Location ID', [InputRequired()],choices=[], coerce=lambda x: x if x == ' ' else  int(x))
    product_id = SelectField('Product ID', [InputRequired()], choices=[], coerce=lambda x: x if x == ' ' else  int(x))
    quantity = IntegerField('Product Quantity', [InputRequired()])