import json

# Converts numpy array to JSON-friendly (adds commas between values)
def format_numpy_as_json_list(array):
        astring = '['
        for element in array:
            astring += f'{element:.3f}, '
               
        # Now chop off that last space and comma before ending
        astring = astring[0:-2]    
        astring += ']'
        return astring

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

def base_graph_params(pulse_type):
    params = json.dumps([])

    if pulse_type == 'sinc':
        params = json.dumps([{"name": "npts", "val": 128, "min": 28, "max": 512, "step": 16},
                            {"name": "duration", "val": 2.0, "min": 0.1, "max": 20.0, "step": 0.1},
                            {"name": "nlobes", "val": 5, "min": 1, "max": 11, "step": 1},
                            {"name": "window alpha", "val": 1, "min": 0.5, "max": 1, "step": 0.05}])
    elif pulse_type == 'gauss':
        params = json.dumps([{"name": "npts", "val": 128, "min": 28, "max": 512, "step": 16},
                            {"name": "duration", "val": 2.0, "min": 0.1, "max": 20.0, "step": 0.1},
                            {"name": "trunc", "val": 3.0, "min": 0.5, "max": 10, "step": 0.5}])
        
    elif pulse_type == 'square':
        params = json.dumps([{"name": "npts", "val": 128, "min": 28, "max": 512, "step": 16},
                            {"name": "duration", "val": 2.0, "min": 0.1, "max": 20.0, "step": 0.1}])

    elif pulse_type == 'HSn':
        params = json.dumps([{"name": "npts", "val": 128, "min": 28, "max": 512, "step": 16},
                            {"name": "duration", "val": 2.0, "min": 0.1, "max": 20.0, "step": 0.1},
                            {"name": "r value", "val": 10, "min": 0.1, "max": 100, "step": 0.1},
                            {"name": "n exponent", "val": 1, "min": 1, "max": 20, "step": 0.1},
                            {"name": "trunc", "val": 0.01, "min": 0.0001, "max": 0.1, "step": 0.0001}])

    return params

def base_sim_params(pulse_type):
    params = json.dumps([])

    if pulse_type != 'none':
        params = json.dumps([{"name": "simulation bw", "val": 4000, "min": 100, "max": 10000, "step": 100},
                             {"name": "offset steps", "val": 101, "min": 30, "max": 1000, "step": 10},
                             {"name": "gamma b1 max", "val": 353, "min": 30, "max": 1000, "step": 5},
                             {"name": "T1", "val": 1000, "min": 100, "max": 10000, "step": 100},
                             {"name": "T2", "val": 1000, "min": 100, "max": 10000, "step": 100},
                             ])

    return params
