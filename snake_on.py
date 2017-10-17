#!/home/pi/venv/home_control/bin/python
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
pin = 4  # Fluorescent lamp in snake tank

GPIO.setup(pin, GPIO.OUT)
GPIO.setup(pin, GPIO.LOW)
print("Let there be light!")
time.sleep(2)
