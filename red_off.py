#!/home/pi/venv/home_control/bin/python
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
pin = 17  # Red LED strip in snake tank

GPIO.setup(pin, GPIO.OUT)
GPIO.setup(pin, GPIO.HIGH)
print("Darkness falls again.")
time.sleep(2)
