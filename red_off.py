#!/home/pi/venv/home_control/bin/python
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
pin = 17  # Red LED strip in snake tank

GPIO.setup(pin, GPIO.OUT)
GPIO.setup(pin, GPIO.HIGH)
print("And the world becomes just a little more red.")
time.sleep(2)
