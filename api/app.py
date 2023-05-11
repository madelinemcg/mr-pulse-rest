from flask import Flask, request

app = Flask(__name__, static_url_path="", static_folder='../client/build')

def graph_data(pulse_type):
    if pulse_type == 'sinc':
        data = [4, 2, 1]
        return str(data)
    if pulse_type == 'gauss':
        data = [5, 3, 7]
        return str(data)
    else:
        return "[]"

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/simulation')
def sim_page():
    return app.send_static_file('index.html')

@app.route('/pulse')
def get_pulse():
    return {
        'type': 'sinc',
        'graph_data': graph_data('sinc')
    }

@app.route("/pulsechange", methods=['POST', 'GET'])
def change_pulse():
    pulse_type = request.get_json(silent=True)['type']

    return {'type': pulse_type,
            'graph_data': graph_data(pulse_type)
            } 
