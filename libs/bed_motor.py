import time
from . import drive_linear_motor as DriveMotor

HatMdd10 = DriveMotor.HatMdd10(67)

LOAD_FULL = 2.5
LOAD_HALF = 1.5
LOAD_BREAK = 0.3


def left90():
    print("Call: left90()")
    # ซ้าย-เลื่อนออก
    HatMdd10.m2AB()
    time.sleep(LOAD_FULL)
    # ซ้าย-หยุด
    HatMdd10.m2Is0()
    time.sleep(LOAD_BREAK)
    print("End-motor.")


def right90():
    print("Call: right90()")
    # ขวา-เลื่อนออก
    HatMdd10.m1AB()
    time.sleep(LOAD_FULL)
    # ขวา-หยุด
    HatMdd10.m1Is0()
    time.sleep(LOAD_BREAK)
    print("End-motor.")


def main():
    print("Debug-mode:")
    left90()
    # right90()
    print("END-Debug.")


if __name__ == "__main__":
    main()
