import speech_recognition as sr
import RPi.GPIO as GPIO
import time

# Set up GPIO
LED_PIN = 17  # Change this to the GPIO pin you are using
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)

def turn_on_led():
    GPIO.output(LED_PIN, GPIO.HIGH)
    print("LED turned on")

def turn_off_led():
    GPIO.output(LED_PIN, GPIO.LOW)
    print("LED turned off")


