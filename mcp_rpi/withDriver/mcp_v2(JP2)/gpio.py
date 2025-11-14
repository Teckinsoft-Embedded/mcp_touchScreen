import RPi.GPIO as GPIO

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
        GPIO.setwarnings(False)

        # Setup input pins
        for pin in INPUT_PINS.values():
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Setup output pins
        for pin in OUTPUT_PINS.values():
            GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

    def gpioGet(self):
        return sum((GPIO.input(pin) << i) for i, pin in enumerate(INPUT_PINS.values()))

    def gpioSet(self, gpio_value):
        for i, pin in enumerate(OUTPUT_PINS.values()):
            GPIO.output(pin, GPIO.HIGH if (gpio_value & (1 << i)) else GPIO.LOW)

    def gpio_release(self):
        print("Releasing GPIOs...")
        for pin in OUTPUT_PINS.values():
            GPIO.output(pin, GPIO.LOW)
        GPIO.cleanup()
