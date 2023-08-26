from flask import Flask, request, json
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
        'graph_data': graph_data('none', '[]'),
        'graph_params': base_graph_params('none')
    }

# PJB: Adding this function because sometimes (presumably due to a configuration difference)
# The reqests get sent with Content-type = 'text/plain;charset=UTF-9'. Best to fix this
# in the client, but for now, just convert that text to json
def get_json_data_from_request(request):
    # PJB adding code to convert request from text to json if needed
    content_type = request.headers.get('Content-type')
    if content_type.startswith('text'):
        # print(f'*** WARNING: Expecting json, getting request with Content-type of {content_type}')
        json_data = json.loads(request.data)
    else:
        json_data = request.get_json(silent=True)

    return json_data

@app.route("/pulsechange", methods=['POST', 'GET'])
def change_pulse():

    json_data = get_json_data_from_request(request)
    pulse_type = json_data['type']
    params = base_graph_params(pulse_type)

    return {'type': pulse_type,
            'graph_data': graph_data(pulse_type, params),
            'graph_params': params
            }

@app.route("/pulsegraphparamchange", methods=['POST', 'GET'])
def change_graph_param():
    json_data = get_json_data_from_request(request)
    pulse_type = json_data['type']
    params = (json_data['graph_params'])

    return {
            'graph_params': params,
            'graph_data': graph_data(pulse_type, params)
            }

