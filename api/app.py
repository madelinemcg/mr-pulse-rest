from flask import Flask, request, json
from graphUtils import graph_data
from simUtils import simulate_effect_of_rf_pulse
from baseUtils import base_graph_params, base_sim_params, get_json_data_from_request

app = Flask(__name__, static_url_path="", static_folder='../client/build')

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/simulation')
def sim_page():
    return app.send_static_file('index.html')

@app.route('/pulse')
def get_pulse():
    print(base_sim_params('none'))
    return {
        'type': 'none',
        'graph_data': graph_data('none', '[]'),
        'graph_params': base_graph_params('none'),
        'sim_data': simulate_effect_of_rf_pulse('none', '[]', '[]', '[]'),
        'sim_params': base_sim_params('none')
    }

@app.route("/pulsechange", methods=['POST', 'GET'])
def change_pulse():

    json_data = get_json_data_from_request(request)
    pulse_type = json_data['type']
    params = base_graph_params(pulse_type)
    sim_params = base_sim_params(pulse_type)
    new_graph_data = graph_data(pulse_type, params)

    return {'type': pulse_type,
            'graph_data': new_graph_data,
            'graph_params': params,
            'sim_params': sim_params,
            'sim_data': simulate_effect_of_rf_pulse(pulse_type, new_graph_data, params, sim_params),
            }

@app.route("/pulsegraphparamchange", methods=['POST', 'GET'])
def change_graph_param():
    json_data = get_json_data_from_request(request)
    pulse_type = json_data['type']
    params = json_data['graph_params']
    graph_data = graph_data(pulse_type, params)
    sim_params = json_data['sim_params']

    return {
            'graph_params': params,
            'graph_data': graph_data,
            'sim_data': simulate_effect_of_rf_pulse(pulse_type, graph_data, params, sim_params)
            }

@app.route("/pulsesimparamchange", methods=['POST', 'GET'])
def change_sim_param():
    json_data = get_json_data_from_request(request)
    pulse_type = json_data['type']
    params = json_data['graph_params']
    graph_data = json_data['graph_data']
    sim_params = json_data['sim_params']

    return {
            'sim_params': sim_params,
            'sim_data': simulate_effect_of_rf_pulse(pulse_type, graph_data, params, sim_params)
            }
