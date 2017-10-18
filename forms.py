from flask_wtf import FlaskForm
from wtforms import BooleanField


class ControlForm(FlaskForm):
    snake_light = BooleanField()
    red_light = BooleanField()
