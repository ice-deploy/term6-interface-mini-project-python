import atexit

import time
import RPi.GPIO as GPIO


# set ENV:
PWM_DUTY_CYCLE = 100
PWM_FREQUENCY = 100
PWM_TIME_WAIT = 0.07


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

    def __init__(self, f=PWM_FREQUENCY, dutyCycle=PWM_DUTY_CYCLE):
        print("__init__")
        # init-dutyCycle
        self.dutyCycle = dutyCycle
        # init-frequency
        self.frequency = f
        # init-waitHardware
        self.waitHardwareUpdate = PWM_TIME_WAIT
        # init-pin
        self.__pin_dir1 = 26
        self.__pin_dir2 = 24
        self.__pin_pwm1 = 12
        self.__pin_pwm2 = 13
        # setup-GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        # setup-pin
        GPIO.setup(self.__pin_dir1, GPIO.OUT)		# set pin as output
        GPIO.setup(self.__pin_dir2, GPIO.OUT)		# set pin as output
        GPIO.setup(self.__pin_pwm1, GPIO.OUT)		# set pin as output
        GPIO.setup(self.__pin_pwm2, GPIO.OUT)		# set pin as output
        # init-PWM
        self.m1 = GPIO.PWM(self.__pin_pwm1, self.frequency)			# set pwm for M1
        self.m2 = GPIO.PWM(self.__pin_pwm2, self.frequency)			# set pwm for M2
        # init-motoeState (ตั้งเป็น True เพราะ เริ่มต้น จะเคลียก่อน)
        self.stateM1 = 1
        self.stateM2 = 1
        # clear-oldState-GPIO
        self.stopAll()
        # Listen-Cleanup()
        atexit.register(self.cleanup)

    # wait Hardware
    def waitHardware(self):
        time.sleep(self.waitHardwareUpdate)

    # motor-All zero
    def mZero(self):
        self.m1Is0()
        self.m2Is0()

    # motor-1 function
    def m1Is0(self):
        self.m1.stop()
        GPIO.output(self.__pin_dir1, GPIO.LOW)
        # update state
        self.stateM1 = 0
        self.waitHardware()

    def m1AB(self):
        self.m1.start(self.dutyCycle)
        GPIO.output(self.__pin_dir1, GPIO.LOW)
        # update state
        self.stateM1 = 1
        self.waitHardware()

    def m1BA(self):
        self.m1.start(self.dutyCycle)
        GPIO.output(self.__pin_dir1, GPIO.HIGH)
        # update state
        self.stateM1 = 1
        self.waitHardware()

    # motor-2 function
    def m2Is0(self):
        self.m2.stop()
        GPIO.output(self.__pin_dir2, GPIO.LOW)
        # update state
        self.stateM2 = 0
        self.waitHardware()

    def m2AB(self):
        self.m2.start(self.dutyCycle)
        GPIO.output(self.__pin_dir2, GPIO.LOW)
        # update state
        self.stateM2 = 1
        self.waitHardware()

    def m2BA(self):
        # control motor
        self.m2.start(self.dutyCycle)
        GPIO.output(self.__pin_dir2, GPIO.HIGH)
        # update state
        self.stateM2 = 1
        self.waitHardware()

    def _stopPwm(self):
        self.m1.stop()
        self.m2.stop()

    def _stopDir(self):
        GPIO.output(self.__pin_dir1, GPIO.LOW)
        GPIO.output(self.__pin_dir2, GPIO.LOW)

    def stopAll(self):
        self._stopPwm()
        self._stopDir()
        self.stateM1 = 0
        self.stateM2 = 0
        self.waitHardware()

    def cleanup(self):
        print("Running cleanup...")
        try:
            self.stopAll()
            GPIO.cleanup()  # this ensures a clean exit
        except Exception as err:
            print("!!!!HatMdd10::cleanup() more one times..")
            print(str(err.args))
        except:
            print("!!!!HatMdd10::cleanup() more one times..")
            print("Other error when HatMdd10::cleanup()!")
        print("HatMdd10::cleanup()")

    # DEBUG-only
    def _testErr(self):
        raise AttributeError('HatMdd10::testErr()')


def main():
    print("DEBUG-Linear-Motor:")

    motor = HatMdd10(PWM_FREQUENCY, PWM_DUTY_CYCLE)
    try:
        while True:
            x = input("enter input:")
            print("input: " + x)
            # testErr
            if x == "err":
                motor._testErr()

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

            print('state of HatMdd10: M1='+str(motor.stateM1) +
                  'M2='+str(motor.stateM2))

    except KeyboardInterrupt:
        print("\n", "CTRL+C")

    except Exception as err:
        print(str(err.args))

    except:
        print("Other error[in Main()] or exception occurred!")

    motor.cleanup()
    print("exit()")


if __name__ == "__main__":
    main()
