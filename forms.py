from wtforms import Form, BooleanField, StringField, PasswordField, validators


class ControlForm(Form):
    snake_light = BooleanField()
    red_light = BooleanField()
