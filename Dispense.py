import RPi.GPIO as GPIO
import time

# Board Setup
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Initializing pins
Pin_7, Pin_8, Pin_9, Pin_10  = 3, 5, 7, 8

#Pin_11, Pin_12, Pin_13 = 10, 12, 11

Punching_Switch, Cutter_Switch, Aloo_Switch, Chick_Switch = 13, 36, 38, 35

Sweet_Switch, Spicy_Switch, Swnsp_Switch = 15, 16, 18

# FeedB_Ons, Empty_pin_2, = 24, 22

# Pin_5 Direction Pin_6 Step
Pin_5, Pin_6 = 31, 33

# Pin Setup
GPIO.setup(Pin_7, GPIO.IN)
GPIO.setup(Pin_8, GPIO.IN)
GPIO.setup(Pin_9, GPIO.IN)
GPIO.setup(Pin_10, GPIO.IN)
# GPIO.setup(Pin_11, GPIO.IN)
# GPIO.setup(Pin_12, GPIO.IN)
# GPIO.setup(Pin_13, GPIO.IN)

# GPIO.setup(Stop_Servo, GPIO.OUT)
GPIO.setup(Pin_5, GPIO.OUT)
GPIO.setup(Pin_6, GPIO.OUT)
# GPIO.setup(Punching_Switch, GPIO.OUT)
# GPIO.setup(Cutter_Switch, GPIO.OUT)
# GPIO.setup(Aloo_Switch, GPIO.OUT)
# GPIO.setup(Chick_Switch, GPIO.OUT)
# GPIO.setup(Sweet_Switch, GPIO.OUT)
# GPIO.setup(Spicy_Switch, GPIO.OUT)
# GPIO.setup(Swnsp_Switch, GPIO.OUT)

# Feedback pin from onions module...
# GPIO.setup(FeedB_Ons, GPIO.IN)

# GPIO.output(Cutter_Switch, False)
# GPIO.output(Aloo_Switch, False)
# GPIO.output(Punching_Switch, False)
# GPIO.output(Chick_Switch, False)
# GPIO.output(Sweet_Switch, False)
# GPIO.output(Spicy_Switch, False)
# GPIO.output(Swnsp_Switch, False)
# GPIO.output(Stop_Servo, False)


def integrate():
    # print(sweet, spicy, swnsp)
    print("Slider is Going to Home Position")
    # Setting to home position....
    while (GPIO.input(Pin_7) == True):
        GPIO.output(Pin_5, False)
        GPIO.output(Pin_6, True)
        time.sleep(0.0001)
        GPIO.output(Pin_6, False)
        time.sleep(0.001)
    # Set at home...

    print("Slider is at Home Position")
    print("Slider is at Position ' 1 '")
    time.sleep(1)
    print("Slider movement started forward")

    # GPIO.output(Stop_Servo, True)
    # time.sleep(1)
    # print("Servo opened...")
    # GPIO.output(Stop_Servo, False)
    # time.sleep(2)

    # list_pins = [Pin_7, Pin_8, Pin_9, Pin_10, Pin_11, Pin_12, Pin_13]
    list_pins = [Pin_7, Pin_8, Pin_9, Pin_10]

    for i in range(4):
        while GPIO.input(list_pins[i]) == True:
            pass

        GPIO.output(Pin_5, True)
        # print("Slider is going towards: {}".format(list_pins[i + 1]))

        while GPIO.input(list_pins[i + 1]) == True:
            # print("At: ",list_pins[i+1])
            GPIO.output(Pin_6, True)
            time.sleep(0.0001)
            GPIO.output(Pin_6, False)
            time.sleep(0.001)

        if list_pins[i + 1] == Pin_8:
            print(Pin_8)
            print("Idly Placing Started")
            # GPIO.output(Punching_Switch, True)
            # time.sleep(1)
            # GPIO.output(Punching_Switch, False)
            time.sleep(5)
            print("Idly Placing Completed")

        if (list_pins[i + 1] == Pin_9):
            ''' and (onions == 1):'''
            print(Pin_9)
            print("Chutney, Sambar and Spoon dispensing started")
            # GPIO.output(Cutter_Switch, True)
            # time.sleep(1)
            # GPIO.output(Cutter_Switch, False)
            # print(GPIO.input(FeedB_Ons))
            # while (GPIO.input(FeedB_Ons) == True):
            #     time.sleep(0.001)
                # print("Feed back from onion awaited...")
            time.sleep(2)
            print("Feedback arrived...")
            print("Chutney, Sambar and Spoon dispensing completed")

        if (list_pins[i + 1] == Pin_10):
            # and (aloo == 1):
            print(Pin_10)
            print("Plate at the User...")
            time.sleep(3)
            print("Plate delivered...")

        # print("Slider is at: {}".format(i + 1))
        # time.sleep(0.25)  # Time delay at each switch

    print("Slider is going to HOME position")
    while (GPIO.input(Pin_7) == True):
        GPIO.output(Pin_5, False)
        GPIO.output(Pin_6, True)
        time.sleep(0.0001)
        GPIO.output(Pin_6, False)
        time.sleep(0.001)
    print("Slider is at Home Position")

    # GPIO.output(Enable_Pin, True)
    return
integrate()