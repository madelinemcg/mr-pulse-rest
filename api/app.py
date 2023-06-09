from flask import Flask, request
from utils import graph_data, base_graph_params

app = Flask(__name__, static_url_path="", static_folder='../client/build')

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/simulation')
def sim_page():
    return app.send_static_file('index.html')

@app.route('/pulse')
def get_pulse():
    return {
        'type': 'none',
        'graph_data': graph_data('none'),
        'graph_params': base_graph_params('none')
    }

@app.route("/pulsechange", methods=['POST', 'GET'])
def change_pulse():
    pulse_type = request.get_json(silent=True)['type']

    return {'type': pulse_type,
            'graph_data': graph_data(pulse_type),
            'graph_params': base_graph_params(pulse_type)
            }
