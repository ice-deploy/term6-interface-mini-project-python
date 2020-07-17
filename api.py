from flask import Flask, json, request
import libs.bed_motor as BedMotor

# import sys

# # init-Flask:
# sudo apt-get install python3-pip python3-dev 
# sudo apt-get install python3-venv

# python3 -m venv env

# source env/bin/activate

# pip install uwsgi flask

# #check python-version
# python --version
# pip freeze

'''
v1(control-from-app)
| api.py -> bed_motor.py(extend-M(HatMdd10)]) 
                    -> drive_linear_motor.py(M[1,2][A,B])

Exception-list:
    - show //response and show in APP(Color=Yellow)
    - Bug //response and show in APP(Color=Red)
'''


# NOTE: path-API
#    # /debug/ [1a,1b,10,  2a,2b,20, f167, f2[ความถี่ Hz] 

HatMdd10 = BedMotor.HatMdd10

api = Flask(__name__)
# Flask-Env:
# # on windows: set FLASK_APP=api.py
# # on Linux: export FLASK_APP=api.py

# # on Linux: export FLASK_ENV=development
# # on Linux: export FLASK_APP=bedmotor.py

# Debug Mode:
# # export FLASK_ENV=development
# run:
# # flask run
# # flask run --host=0.0.0.0

# python--import
# https://docs.python.org/3/tutorial/modules.html#intra-package-references
# from . import echo
# from .. import formats
# from ..filters import equalizer


# /debug/1a
@api.route('/debug/<mode>', methods=['GET'])
def get_debug(mode):
    print("GET: /debug/"+mode)

    # motor-1
    if mode == "1a":
        # attrs = vars(HatMdd10)
        # print(attrs)
        HatMdd10.m1AB()
    elif mode == "1b":
        HatMdd10.m1BA()
    elif mode == "10":
        HatMdd10.m1Is0()

    # motor-2
    elif mode == "2a":
        HatMdd10.m2AB()
    elif mode == "2b":
        HatMdd10.m2BA()
    elif mode == "20":
        HatMdd10.m2Is0()
        
    elif mode[0] == "f":
        if mode[1] == "1":
            HatMdd10.changeFrequency1(int(mode[2:]))
        elif mode[1] == "2":
            HatMdd10.changeFrequency2(int(mode[2:]))

    return json.dumps({"dataStatus": "success"})


if __name__ == '__main__':
    # api.run()
    api.run(host='0.0.0.0')
