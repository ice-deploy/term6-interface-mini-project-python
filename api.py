from flask import Flask, json, request
from threading import Thread
import libs.drive_linear_motor as BedMotor


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
#    # /debug/ [1a=rf,1b=rb,10=r0], [2a=lf,2b=lb,20=l0]


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

    # Enable Cors for web-browser test
    @app.after_request
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

    # a simple page that says hello
    @app.route('/')
    def hello():
        print("GET: /index")
        return 'Hello, World!'

    # http://127.0.0.1:5000/stop
    @app.route('/stop', methods=['GET'])
    def stop():
        print("GET: /stop")
        print("Shutdown: with Hard-STOP API(/stop")
        shutdown()
        return myRes({"dataStatus": "success", 'data': 'stoped'})

    # /debug/ []
    @app.route('/debug/<command>', methods=['GET'])
    def get_debug(command):
        print("GET: /debug/"+command)

        # motor-1
        if command == "1a":
            HatMdd10.m1AB()
            message = 'rf'
        elif command == "1b":
            HatMdd10.m1BA()
            message = 'rb'
        elif command == "10":
            HatMdd10.m1Is0()
            message = 'r0'

        # motor-2
        elif command == "2a":
            HatMdd10.m2AB()
            message = 'lf'
        elif command == "2b":
            HatMdd10.m2BA()
            message = 'lb'
        elif command == "20":
            HatMdd10.m2Is0()
            message = 'l0'

        else:
            return myRes({"dataStatus": "error", 'message': 'not command: ' + command}, 404)

        return myRes({"dataStatus": "success", "message": message})

    return app


def main():
    HatMdd10 = BedMotor.HatMdd10()
    try:
        app = create_app(HatMdd10)
        app.run(host='0.0.0.0')
    except Exception as err:
        print(str(err.args))
    except:
        print('some Err: server is Stoped.')

    HatMdd10.cleanup()


if __name__ == '__main__':
    main()
