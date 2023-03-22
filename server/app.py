from flask import Flask, request, send_from_directory

app = Flask(__name__, static_url_path="", static_folder='../client/build')

@app.route("/")
def home():
    return app.send_static_file('index.html')


@app.post('/pulsegen')
def test():

    pulse_type = request.json['type']
    if pulse_type == 'sinc':
        return {'type': 'sinc',
                'data': [0, -0.1, -0.2, -0.1, 0, 0.2, 0.5, 0.9, 1.0, 0.9, 0.5, 0.2, 0, -0.1, -0.2, -0.1, 0] }        
    elif pulse_type == 'gauss':
        return {'type': 'gauss',
                'data': [0, 0.1, 0.2, 0.5, 0.9, 1.0, 0.9, 0.5, 0.2, 0.1, 0] }        
    else:
        # Return an error code, like 400?
        return 'Unrecognized pulse type'
