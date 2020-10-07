import time
import requests
from picamera import PiCamera

import RPi.GPIO as GPIO

# Use "GPIO" pin numbering
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Pin definitions
Pin_11, Pin_13, Pin_38 = 11 ,13, 38

# Set LED pin as output
GPIO.setup(Pin_11, GPIO.OUT)
GPIO.setup(Pin_13, GPIO.OUT)
GPIO.setup(Pin_38, GPIO.IN)

def integrate():
    print("sending signal to plate picking")
    GPIO.output(Pin_11, False)
    GPIO.output(Pin_13, False)
    GPIO.output(Pin_11, True)
    GPIO.output(Pin_13, True)# Turn LED on
    time.sleep(2)                   # Delay for 2 second
    GPIO.output(Pin_11, False)
    GPIO.output(Pin_13, False)
    return


def integrate3():
    while (GPIO.input(Pin_38)==True):
        print("waitng for IR signal")
    print("order completed")
    try:
        camera = PiCamera() 
        #camera.start_preview()
        camera.rotation = 180
        camera.brightness =50
        #camera.annotate_text = "Hai idli machine user"
        print("camera captured")
        camera.resolution = (220, 130)
        camera.zoom = (0.1, 0.01, 1, 1)
        time.sleep(1)
        camera.capture('Pictures/order.png')
        #camera.stop_preview()
        camera.close()
        return
    except Exception:
        print("not captured")
        return
#integrate3()
#integrate()
