import numpy as np

# Converts numpy array to JSON-friendly (adds commas between values)
def format_numpy_as_json_list(array):
        astring = '['
        for element in array:
            astring += f'{element:.3f}, '
               
        # Now chop off that last space and comma before ending
        astring = astring[0:-2]    
        astring += ']'
        return astring

# Redirects calculation based on pulse type
def graph_data(pulse_type):
    xdata = np.empty([0, 0], dtype=float)
    ydata = np.empty([0, 0], dtype=float)

    npts = 16 # very short! Typically >200
    duration = 2 # milliseconds

    # Calculate time axes. xdata is time, from 0 to duration.
    # Tau is normalized from -1 to 1
    tau = np.linspace(-1.0, 1.0, npts)
    xdata = np.linspace(0, duration, npts)


    if pulse_type == 'sinc':
        nlobes = 5
        ydata = np.sin((nlobes+1) * np.pi * tau ) / ((nlobes+1) * np.pi * tau)
        ydata[np.isnan(ydata)] = 1.0 # correct div by zero error

    elif pulse_type == 'gauss':
        # Here is the calculation of the guassian shape
        truncation_sigma = 3
        ydata = np.exp(-0.5 * (tau * truncation_sigma)**2)

    else:
        ydata = np.array([4.01, 2.0, 1.3, 1])
        xdata = np.array([1, 2, 3, 4])

    xdata = format_numpy_as_json_list(xdata)
    ydata = format_numpy_as_json_list(ydata)

    return {
        # Note: if np thinks the arrays are floats it will call this formatter. 
        'xdata': xdata,
        'ydata': ydata
    }   

def base_graph_params(pulse_type):
    params = "[]"

    if pulse_type == 'sinc':
        # Sorry for the super long line, Python doesn't like multi-line JSON
        params = '[{"name": "npts", "val": 128, "min": 28, "max": 512, "step": 16}, {"name": "duration", "val": 2.0, "min": 0.1, "max": 20.0, "step": 0.1}, {"name": "nlobes", "val": 5, "min": 1, "max": 11, "step": 1}, {"name": "window_alpha", "val": 1.0, "min": 0.001, "max": 1, "step": 0.001}]'
    elif pulse_type == 'gauss':
        params = '[{"name": "npts", "val": 128, "min": 28, "max": 512, "step": 16}, {"name": "duration", "val": 2.0, "min": 0.1, "max": 20.0, "step": 0.1}, {"name": "trunc", "val": 3.0, "min": 0.5, "max": 10, "step": 0.5}]'

    return params
