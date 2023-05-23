from flask import Flask, request
from utils import graph_data

app = Flask(__name__, static_url_path="", static_folder='../client/build')

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/simulation')
def sim_page():
    return app.send_static_file('index.html')

# Set type using this syntax: http://127.0.0.1:5000/pulse?type=sinc
@app.route('/pulse')
def get_pulse():

    type = request.args.get('type')
    print(f'type is {type}')
    return {
        'type': type,
        'graph_data': graph_data(type)
    }

@app.route("/pulsechange", methods=['POST', 'GET'])
def change_pulse():
    pulse_type = request.get_json(silent=True)['type']

    return {'type': pulse_type,
            'graph_data': graph_data(pulse_type)
            } 
