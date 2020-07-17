import atexit
import os

import RPi.GPIO as GPIO


class HatMdd10:
    '''
    NOTE:
        pwm     |   dir     |   A       |   B
        ---------------------------------
        LOW     |   x       |   LOW     |   LOW
        HIGH    |   LOW     |   HIGH    |   LOW
        HIGH    |   HIGH    |   LOW     |   HIGH

    params:
        f = ความถี่ Hz //frequency

    '''

    def __init__(self, f):
        print("__init__")
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.__pin_dir1 = 26
        self.__pin_dir2 = 24
        self.__pin_pwm1 = 12
        self.__pin_pwm2 = 13
        # init-pin
        GPIO.setup(self.__pin_dir1, GPIO.OUT)		# set pin as output
        GPIO.setup(self.__pin_dir2, GPIO.OUT)		# set pin as output
        GPIO.setup(self.__pin_pwm1, GPIO.OUT)		# set pin as output
        GPIO.setup(self.__pin_pwm2, GPIO.OUT)		# set pin as output
        # init-PWM
        self.m1 = GPIO.PWM(self.__pin_pwm1, f)			# set pwm for M1
        self.m2 = GPIO.PWM(self.__pin_pwm2, f)			# set pwm for M2
        self.m1.start(0)
        self.m2.start(0)
        # Listen-Cleanup()
        atexit.register(self.cleanup)

    def cleanup(self):
        print("Running cleanup...")
        self.clearAll()

    # motor-All zero
    def mZero(self):
        self.m1Is0()
        self.m2Is0()

    # motor-1 function
    def m1Is0(self):
        self.m1.ChangeDutyCycle(0)
        GPIO.output(self.__pin_dir1, GPIO.LOW)

    def m1AB(self):
        self.m1.ChangeDutyCycle(25)
        GPIO.output(self.__pin_dir1, GPIO.LOW)

    def m1BA(self):
        self.m1.ChangeDutyCycle(25)
        GPIO.output(self.__pin_dir1, GPIO.HIGH)

    # motor-2 function
    def m2Is0(self):
        self.m2.ChangeDutyCycle(0)
        GPIO.output(self.__pin_dir2, GPIO.LOW)

    def m2AB(self):
        self.m2.ChangeDutyCycle(25)
        GPIO.output(self.__pin_dir2, GPIO.LOW)

    def m2BA(self):
        self.m2.ChangeDutyCycle(25)
        GPIO.output(self.__pin_dir2, GPIO.HIGH)

    # changeFrequency[1,2]
    def changeFrequency1(self, newFrequency):
        self.m1.ChangeFrequency(newFrequency)

    def changeFrequency2(self, newFrequency):
        self.m2.ChangeFrequency(newFrequency)

    # clearGPIO
    def clearPwm(self):
        self.m1.stop()
        self.m2.stop()

    def clearDir(self):
        GPIO.output(self.__pin_dir1, GPIO.LOW)
        GPIO.output(self.__pin_dir2, GPIO.LOW)

    def clearAll(self):
        self.clearPwm()
        self.clearDir()
        GPIO.cleanup()  # this ensures a clean exit


def main():
    print("Drive-Linear-Motor:")

    motor = HatMdd10(67)
    try:
        while True:
            x = input("enter input:")
            print("input: " + x)
            # motor-1
            if x == "1a":
                motor.m1AB()
            elif x == "1b":
                motor.m1BA()
            elif x == "10":
                motor.m1Is0()

            # motor-2
            elif x == "2a":
                motor.m2AB()
            elif x == "2b":
                motor.m2BA()
            elif x == "20":
                motor.m2Is0()

            elif x[0] == "f":
                if x[1] == "1":
                    motor.changeFrequency1(int(x[2:]))
                elif x[1] == "2":
                    motor.changeFrequency2(int(x[2:]))

    except KeyboardInterrupt:
        print("\n", "CTRL+C")

    except:
        print("Other error or exception occurred!")

    finally:
        # motor.clearAll()
        print("exit()")


if __name__ == "__main__":
    main()
