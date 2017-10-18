from flask import Flask, render_template, request
import os
import re
from subprocess import call, check_output

from forms import ControlForm

app = Flask(__name__)
app.secret_key = os.environ.get('CONTROL_SECRET_KEY')


def get_states():
    # Pin numbers here are based on the WiringPi package
    red_light_pin = '0'
    fluorescent_light_pin = '7'
    # Read the state of the pin and parse the output for the number returned
    red_state = re.findall(r'\d+', check_output(['gpio', 'read', red_light_pin]).decode('utf-8'))[0]
    fluorescent_state = re.findall(r'\d+', check_output(['gpio', 'read', fluorescent_light_pin]).decode('utf-8'))[0]
    # Convert the strings into integers
    red_state = int(red_state)
    fluorescent_state = int(fluorescent_state)
    # Flip the states because 1 equals off, which makes less intuitive sense
    states = {'red': not red_state, 'fluorescent': not fluorescent_state}
    return states


@app.route('/', methods=['GET', 'POST'])
def home():
    form = ControlForm()
    states = get_states()
    if request.method == 'GET':
        form.snake_light.data = states['fluorescent']
        form.red_light.data = states['red']
    if form.validate_on_submit():
        form_fluorescent = form.snake_light.data
        form_red = form.red_light.data
        if form_fluorescent != states['fluorescent']:
            # Only need to do something if the form option doesn't match the current state of the light
            if form_fluorescent:
                call(['/home/pi/controls/snake_on.py'])
            else:
                call(['/home/pi/controls/snake_off.py'])
        if form_red != states['red']:
            if form_red:
                call(['/home/pi/controls/red_on.py'])
            else:
                call(['/home/pi/controls/red_off.py'])
    return render_template('control_home.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
