import threading
import atexit
import time

from flask import Flask, json, request

import libs.drive_linear_motor as BedMotor

# API: v2.1.6
'''
- protect access 'drive_linear_motor.py' in same time.
- edit-path from '/debug/<command>' to '/api/<command>'
'''

# Flask-Env:
# # on windows: set FLASK_APP=api.py
'''
on Linux: export FLASK_APP=api.py
on Linux: export FLASK_ENV=development

python3 api.py
'''

# run:
# # flask run
# # flask run --host=0.0.0.0

# NOTE: flask-API
#    # /stop //for Stop Server (ฉุกเฉิน)
#    # /api/ [1a=rf,1b=rb,10=r0], [2a=lf,2b=lb,20=l0]

LIMIT_MOTOR_RUNNING = 0.7  # Seconds
LIMIT_REQUEST_FREQUENCY = 0.2  # Seconds

lastTimeReq = float(0)

# lock to control access to variable
dataReqLock = threading.Lock()
# thread handler
listThread1 = []
listThread2 = []


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def shutdown():
    shutdown_server()
    return 'Server shutting down...'


def create_app(HatMdd10):
    # https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/
    app = Flask(__name__)

    def debounce() -> bool:
        global lastTimeReq
        END = time.time()
        total_time = float(END - lastTimeReq)

        if total_time > float(LIMIT_REQUEST_FREQUENCY):
            return True
        return False

    def doStuffM1Stop():
        global listThread1
        for currentThread in listThread1:
            currentThread.cancel()

    def doStuffM1Is0(HatMdd10):
        with dataReqLock:
            HatMdd10.m1Is0()

    def doStuffM1Start(HatMdd10):
        yourThread = threading.Thread()
        yourThread = threading.Timer(
            LIMIT_MOTOR_RUNNING, doStuffM1Is0, args=[HatMdd10])
        listThread1.append(yourThread)
        yourThread.start()

    def doStuffM2Stop():
        global listThread2
        for currentThread in listThread2:
            currentThread.cancel()

    def doStuffM2Is0(HatMdd10):
        with dataReqLock:
            HatMdd10.m2Is0()

    def doStuffM2Start(HatMdd10):
        yourThread = threading.Thread()
        yourThread = threading.Timer(
            LIMIT_MOTOR_RUNNING, doStuffM2Is0, args=[HatMdd10])
        listThread2.append(yourThread)
        yourThread.start()

    @app.after_request  # cors for Web-Browser
    def after_request(response):
        header = response.headers
        header['Access-Control-Allow-Origin'] = '*'
        return response

    # set response mimetype=JSON
    def myRes(data, headerStatus=200):
        response = app.response_class(
            response=json.dumps(data),
            status=headerStatus,
            mimetype='application/json'
        )
        return response

    # check Server is Running...
    @app.route('/')
    def hello():
        # print("GET: /index")
        return myRes({"dataStatus": "success", 'data': 'Server is Running...'})

    # http://127.0.0.1:5000/stop
    @app.route('/stop', methods=['GET'])
    def stop():
        # print("GET: /stop")
        # print("Shutdown: with Hard-STOP API(/stop")
        # Stop Theard
        doStuffM1Stop()
        doStuffM2Stop()
        # Stop Server-Sevice.
        shutdown()
        return myRes({"dataStatus": "success", 'data': 'stoped'})

    # /api/1a
    @app.route('/api/<command>', methods=['GET'])
    def get_api(command):
        # print("GET: /api/"+command)

        if debounce():
            # motor-1
            if command == "1a":
                # Stop All Thead1-list
                doStuffM1Stop()
                # Start Auto-stop-motor1
                doStuffM1Start(HatMdd10)

                with dataReqLock:
                    HatMdd10.m1AB()
                message = 'rf'

            elif command == "1b":
                # Stop All Thead1-list
                doStuffM1Stop()
                # Start Auto-stop-motor1
                doStuffM1Start(HatMdd10)

                with dataReqLock:
                    HatMdd10.m1BA()
                message = 'rb'

            elif command == "10":
                # Stop All Thead1-list
                doStuffM1Stop()

                with dataReqLock:
                    HatMdd10.m1Is0()
                message = 'r0'

            # motor-2
            elif command == "2a":
                # Stop All Thead2-list
                doStuffM2Stop()
                # Start Auto-stop-motor2
                doStuffM2Start(HatMdd10)

                with dataReqLock:
                    HatMdd10.m2AB()
                message = 'lf'
            elif command == "2b":
                # Stop All Thead2-list
                doStuffM2Stop()
                # Start Auto-stop-motor2
                doStuffM2Start(HatMdd10)

                with dataReqLock:
                    HatMdd10.m2BA()
                message = 'lb'
            elif command == "20":
                # Stop All Thead2-list
                doStuffM2Stop()

                with dataReqLock:
                    HatMdd10.m2Is0()
                message = 'l0'

            else:
                return myRes({"dataStatus": "error", 'message': 'not command: ' + command}, 404)

            return myRes({"dataStatus": "success", "message": message})

        return myRes({"dataStatus": "success", "message": "debounce"})
        # return errRes()


    return app


def main():
    HatMdd10 = BedMotor.HatMdd10()
    try:
        app = create_app(HatMdd10)
        app.run(host='0.0.0.0')
    except Exception as err:
        print(str(err.args))
    except KeyboardInterrupt:
        print("\n", "CTRL+C")
    else:
        print('Err when start-Server: (now)server is Stoped.')

    HatMdd10.cleanup()


if __name__ == '__main__':
    main()
