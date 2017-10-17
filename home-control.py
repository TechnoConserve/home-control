from flask import Flask, render_template, request
import RPi.GPIO as GPIO
from subprocess import call

from forms import ControlForm

app = Flask(__name__)


def get_states():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    red_light_pin = 17
    fluorescent_light = 4
    GPIO.setup(red_light_pin, GPIO.IN)
    GPIO.setup(fluorescent_light, GPIO.IN)
    states = {'red': not GPIO.input(red_light_pin),
              'fluorescent': not GPIO.input(fluorescent_light)}
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
