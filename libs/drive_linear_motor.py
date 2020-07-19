import atexit
import os

import time
# import sqlite3
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

    # def connDB(self):
    #     DATABASE = 'database.sqlite'
    #     conn = sqlite3.connect(DATABASE)
    #     conn.row_factory = lambda c, r: dict(
    #         zip([col[0] for col in c.description], r))

    #     return conn

    # def isRunning(self, c):
    #     c.execute("SELECT * FROM settings WHERE key=?", ('isRunning',))
    #     row = c.fetchone()
    #     return row['value']

    # def cancleRunning(self, conn):
    #     c = conn.cursor()
    #     c.execute('UPDATE settings SET value = ? WHERE key = ?',
    #               (1, 'isRunning'))
    #     conn.commit()

    # def waitStopOldProcess(self, conn):
    #     c = conn.cursor()
    #     print('waitStopOldProcess()')
    #     for _ in range(15):
    #         if(self. isRunning(c) == int(False)):
    #             break
    #         self.cancleRunning(conn)
    #         time.sleep(1.1)

    #     print('END-waitStopOldProcess()')

    def __init__(self, f=PWM_FREQUENCY, dutyCycle=PWM_DUTY_CYCLE):
        # DEBUG-only
        self.isCleaned = 0

        print("__init__")
        # conn = self.connDB()

        # raise Exception("Sorry, no numbers below zero", 2)
        # self.waitStopOldProcess(conn)
        # init-dutyCycle
        # self.dutyCycle = 26
        self.dutyCycle = dutyCycle
        # init-frequency
        self.frequency = f
        # init-waitHardware
        self.waitHardwareLong = PWM_TIME_WAIT
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
        # clear-oldState-GPIO
        self.clearPwm()
        self.clearDir()
        # self.m1.stop()
        # self.m2.stop()
        # self.m1.start(0)
        # self.m2.start(0)
        # Listen-Cleanup()
        atexit.register(self.cleanup)

    # def __enter__(self):
    #     GPIO.setmode(GPIO.BCM)
    #     GPIO.setwarnings(False)
    #     # setup-pin
    #     GPIO.setup(self.__pin_dir1, GPIO.OUT)		# set pin as output
    #     GPIO.setup(self.__pin_dir2, GPIO.OUT)		# set pin as output
    #     GPIO.setup(self.__pin_pwm1, GPIO.OUT)		# set pin as output
    #     GPIO.setup(self.__pin_pwm2, GPIO.OUT)		# set pin as output
    #     # init-PWM
    #     self.m1 = GPIO.PWM(self.__pin_pwm1, self.frequency)			# set pwm for M1
    #     self.m2 = GPIO.PWM(self.__pin_pwm2, self.frequency)			# set pwm for M2
    #     self.m1.stop()
    #     self.m2.stop()
    #     return self

    # wait Hardware
    def waitHardware(self):
        time.sleep(self.waitHardwareLong)

    # motor-All zero
    def mZero(self):
        self.waitHardware()
        self.m1Is0()
        self.m2Is0()

    # motor-1 function
    def m1Is0(self):
        self.waitHardware()
        # self.m1.stop()
        self.m1.start(0)
        GPIO.output(self.__pin_dir1, GPIO.LOW)

    def m1AB(self):
        self.waitHardware()
        self.m1.start(self.dutyCycle)
        GPIO.output(self.__pin_dir1, GPIO.LOW)

    def m1BA(self):
        self.waitHardware()
        self.m1.start(self.dutyCycle)
        GPIO.output(self.__pin_dir1, GPIO.HIGH)

    # motor-2 function
    def m2Is0(self):
        self.waitHardware()
        # self.m2.stop()
        self.m2.start(0)
        GPIO.output(self.__pin_dir2, GPIO.LOW)

    def m2AB(self):
        self.waitHardware()
        self.m2.start(self.dutyCycle)
        GPIO.output(self.__pin_dir2, GPIO.LOW)

    def m2BA(self):
        self.waitHardware()
        self.m2.start(self.dutyCycle)
        GPIO.output(self.__pin_dir2, GPIO.HIGH)

    # clearGPIO

    # def __exit__(self, exc_type, exc_value, traceback):
    #     self.cleanup()

    def clearPwm(self):
        self.waitHardware()
        self.m1.stop()
        self.m2.stop()

    def clearDir(self):
        self.waitHardware()
        GPIO.output(self.__pin_dir1, GPIO.LOW)
        GPIO.output(self.__pin_dir2, GPIO.LOW)

    def clearAll(self):
        self.clearPwm()
        self.clearDir()
        GPIO.cleanup()  # this ensures a clean exit

    def cleanup(self):
        print("Running cleanup...")
        try:
            self.clearAll()
            self.testErr()
        except Exception as err:
            print("!!!!HatMdd10::cleanup() more one times..")
            print(str(err.args))
        except:
            print("!!!!HatMdd10::cleanup() more one times..")
            print("Other error when HatMdd10::cleanup()!")
        print("HatMdd10::cleanup()")

    # DEBUG-only
    def testErr(self):
        raise AttributeError('HatMdd10::testErr()')


def main():
    print("DEBUG-Linear-Motor:")

    # HatMdd10(67)
    # motor = HatMdd10(2)
    motor = HatMdd10(PWM_FREQUENCY, PWM_DUTY_CYCLE)
    # with HatMdd10(PWM_FREQUENCY, PWM_DUTY_CYCLE) as motor:
    #     pass
    # cleanup
    # https://raspi.tv/2013/rpi-gpio-basics-3-how-to-exit-gpio-programs-cleanly-avoid-warnings-and-protect-your-pi
    try:
        while True:
            x = input("enter input:")
            print("input: " + x)
            # testErr
            if x == "err":
                motor.testErr()

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
                    motor.cleanup()
                    # motor.changeFrequency1(int(x[2:]))
                elif x[1] == "2":
                    pass
                    # motor.changeFrequency2(int(x[2:]))

    except KeyboardInterrupt:
        # here you put any code you want to run before the program
        # exits when you press CTRL+C
        print("\n", "CTRL+C")  # print value of counter

    except Exception as err:
        print(str(err.args))

    except:
        print("Other error[in Main()] or exception occurred!")

    motor.cleanup()
    print("exit()")


if __name__ == "__main__":
    main()
