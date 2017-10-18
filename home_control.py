from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import re
from subprocess import call, check_output

from forms import ControlForm

app = Flask(__name__)


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
    states = {'red': red_state, 'fluorescent': fluorescent_state}
    GPIO.cleanup()
    return states


@app.route('/', methods=['GET', 'POST'])
def home():
    form = ControlForm()
    states = get_states()
    print('States:', states)
    form.snake_light.data = states['fluorescent']
    form.red_light.data = states['red']
    if request.method == 'POST' and form.validate():
        form_fluorescent = not form.snake_light.data
        form_red = not form.red_light.data
        if form_fluorescent != states['fluorescent']:
            call(['/home/pi/controls/snake_on.py'])
        else:
            call(['/home/pi/controls/snake_off.py'])
        if form_red != states['red']:
            call(['/home/pi/controls/red_on.py'])
        else:
            call(['/home/pi/controls/red_off.py'])
    return render_template('control_home.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
