from flask import Flask, render_template, request
from subprocess import call

from forms import ControlForm

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    form = ControlForm(request.form)
    if request.method == 'POST' and form.validate():
        state = form.snake_light.data
        if state:
            call(['/home/pi/relay/snake_on.py'])
        else:
            call(['/home/pi/relay/snake_off.py'])
    return render_template('control_home.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
