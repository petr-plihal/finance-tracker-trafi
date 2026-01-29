from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

from app.models.database import Category

class CategoryFormMain(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    monthly_budget = ('name', validators=[validators.optional()])

    transactions
    category_rules