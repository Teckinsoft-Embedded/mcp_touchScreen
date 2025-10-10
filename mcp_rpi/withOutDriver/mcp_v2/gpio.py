import RPi.GPIO as GPIO
import time
import threading
from Ethercat import EtherCATInterface  
# Define input and output GPIOs
INPUT_PINS = {
    "DI0": 4, "DI1": 5, "DI2": 6, "DI3": 12,
    "DI4": 13, "DI5": 16, "DI6": 17, "DI7": 18
}

OUTPUT_PINS = {
    "DO0": 19, "DO1": 20, "DO2": 21, "DO3": 22,
    "DO4": 27, "DO5": 26, "DO6": 24, "DO7": 23
}

class GPIOControl:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        
        # Setup input pins
        for pin in INPUT_PINS.values():
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # Setup output pins
        for pin in OUTPUT_PINS.values():
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
        
        self.etc_interface = EtherCATInterface()
        self.shared_lock = threading.Lock()

    def gpio_input_scan(self):
	
        gpio_value = 0
        
        for i, (name, pin) in enumerate(INPUT_PINS.items()):
            if GPIO.input(pin):  # Read GPIO state (1 or 0)
                gpio_value |= (1 << i)  # Set bit if high (1)
        return  gpio_value
        
    def gpio_output_control(self, gpio_value):

        for i, (name, pin) in enumerate(OUTPUT_PINS.items()):
            if gpio_value & (1 << i):
                GPIO.output(pin, GPIO.HIGH)
            else:
                GPIO.output(pin, GPIO.LOW)

    def gpio_release(self):

        for pin in OUTPUT_PINS.values():
            GPIO.output(pin, GPIO.LOW)  
        GPIO.cleanup()
