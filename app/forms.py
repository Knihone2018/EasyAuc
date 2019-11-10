from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import DataRequired


class BidForm(FlaskForm):
    bid_amount = FloatField('bid_amount', validators=[DataRequired()])
    submit = SubmitField('Place Bid')
