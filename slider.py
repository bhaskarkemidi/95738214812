import RPi.GPIO as GPIO
import time

# Board Setup
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Initializing pins
Pin_7, Pin_8, Pin_9, = 3, 5, 7

Pin_5, Pin_6, Enable_Pin  = 11, 13, 15

#Int_i, Int_a = 7, 1

# Pin Setup
GPIO.setup(Pin_7, GPIO.IN)
GPIO.setup(Pin_8, GPIO.IN)
GPIO.setup(Pin_9, GPIO.IN)

GPIO.setup(Pin_5, GPIO.OUT)
GPIO.setup(Pin_6, GPIO.OUT)
GPIO.setup(Enable_Pin, GPIO.OUT)

GPIO.output(Enable_Pin, False)

for i in range(1):
    print("Slider is Going to Home Position")

    while(GPIO.input(Pin_7) == True):
        GPIO.output(Pin_5, False)
        GPIO.output(Pin_6, True)
        time.sleep(0.0008)
        GPIO.output(Pin_6, False)
        time.sleep(0.0008)

    print("Slider is at Home Position")
    time.sleep(2)
    print("Slider movement started forward")

    list_pins = [Pin_7, Pin_8, Pin_9]

    for i in range(2):
        while GPIO.input(list_pins[i])==True:
            pass

        GPIO.output(Pin_5, True)
        print("Slider is going towrds: {}".format(i+1))

        while GPIO.input(list_pins[i+1])==True:
            GPIO.output(Pin_6, True)
            time.sleep(0.001)
            GPIO.output(Pin_6, False)
            time.sleep(0.001)

            if GPIO.input(list_pins[i+1])==False:
                break
        print("Slider is at: {}".format(i+1))
        time.sleep(2)
        
    while(GPIO.input(Pin_7) == True):
        GPIO.output(Pin_5, False)
        GPIO.output(Pin_6, True)
        time.sleep(0.0008)
        GPIO.output(Pin_6, False)
        time.sleep(0.0008)

GPIO.output(Enable_Pin, True)
print("The Carrier is at Home!!!")
