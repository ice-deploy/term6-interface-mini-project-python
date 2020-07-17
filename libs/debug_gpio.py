
import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def setHi(pin: int):
    print("On GPIO:" + str(pin))
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)


def setLow(pin: int):
    print("Off GPIO:" + str(pin))
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)


def delay(timeNumber: int):
    print("sleep: " + str(timeNumber) + " วินาที")
    time.sleep(timeNumber)


def main():
    print("Dev:")

    # cleanup
    # https://raspi.tv/2013/rpi-gpio-basics-3-how-to-exit-gpio-programs-cleanly-avoid-warnings-and-protect-your-pi
    try:
        while True:
            x = input("enter input:")
            if x[0] is "+":
                setHi(int(x[1:]))
            elif x[0] is "-":
                setLow(int(x[1:]))
            elif x[0] is "d":
                delay(int(x[1:]))

    except KeyboardInterrupt:
        # here you put any code you want to run before the program
        # exits when you press CTRL+C
        print("\n", "CTRL+C")  # print value of counter

    except:
        print("Other error or exception occurred!")

    finally:
        GPIO.cleanup()  # this ensures a clean exit
        print("exit()")


if __name__ == "__main__":
    main()
