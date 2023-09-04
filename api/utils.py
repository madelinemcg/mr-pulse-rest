import numpy as np
import scipy
import math
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

# Redirects calculation based on pulse type
def graph_data(pulse_type, params):
    xdata = np.empty([0, 0], dtype=float)
    # Returns both amplitude and phase (radians). Only HSn has non-zero phase
    amp = np.empty([0, 0], dtype=float)
    phs = np.empty([0, 0], dtype=float)

    params = json.loads(params)

    if pulse_type == 'sinc':
        try:
            for pulse_dict in params:
                if pulse_dict["name"] == "npts":
                    npts = pulse_dict["val"]
                elif pulse_dict["name"] == "duration":
                    duration = pulse_dict["val"]
                elif pulse_dict["name"] == "nlobes":
                    nlobes = pulse_dict["val"]
                elif pulse_dict["name"] == "window alpha":
                    window_alpha = pulse_dict["val"]

            # Calculate time axes. xdata is time, from 0 to duration.
            # For sincs, Tau is normalized from -0.5 to 0.5
            tau = np.linspace(-0.5, 0.5, npts)
            xdata = np.linspace(0, duration, npts)

            amp = np.sin((nlobes+1) * np.pi * tau ) / ((nlobes+1) * np.pi * tau)
            amp[np.isnan(amp)] = 1.0 # correct div by zero error
            phs = amp * 0
            
            if window_alpha<1.0:
                window_function = window_alpha + (1-window_alpha) * np.cos(2 * np.pi * tau)
                amp = amp * window_function


        except:
            print("Sinc pulse error, param object contains: ", params)

    elif pulse_type == 'gauss':
        try:
            for pulse_dict in params:
                if pulse_dict["name"] == "npts":
                    npts = pulse_dict["val"]
                elif pulse_dict["name"] == "duration":
                    duration = pulse_dict["val"]
                elif pulse_dict["name"] == "trunc":
                    truncation_sigma = pulse_dict["val"]
            # Calculate time axes. xdata is time, from 0 to duration.
            # Tau is normalized from -1 to 1
            tau = np.linspace(-1.0, 1.0, npts)
            xdata = np.linspace(0, duration, npts)

            amp = np.exp(-0.5 * (tau * truncation_sigma)**2)
            phs = amp * 0

        except:
            print("Gauss pulse error, param object contains: ", params)

    elif pulse_type == 'square':
        try:
            for pulse_dict in params:
                if pulse_dict["name"] == "npts":
                    npts = pulse_dict["val"]
                elif pulse_dict["name"] == "duration":
                    duration = pulse_dict["val"]

            # Calculate time axes. xdata is time, from 0 to duration.
            xdata = np.linspace(0, duration, npts)

            # Amplitude is always 1.0
            amp = xdata*0 + 1.
            phs = amp * 0

        except:
            print("Square pulse error, param object contains: ", params)

    elif pulse_type == 'HSn':
        try:
            for pulse_dict in params:
                if pulse_dict["name"] == "npts":
                    npts = pulse_dict["val"]
                elif pulse_dict["name"] == "duration":
                    duration = pulse_dict["val"]
                elif pulse_dict["name"] == "r value":
                    r_value = pulse_dict["val"]
                elif pulse_dict["name"] == "n exponent":
                    n_exp = pulse_dict["val"]
                elif pulse_dict["name"] == "trunc":
                    trunc_value = pulse_dict["val"]

            # Calculate time axes. xdata is time, from 0 to duration.
            # Tau is normalized from -1 to 1
            BW = r_value / duration # Hz

            ### Make the pulse
            # For HSn the dummy time variable tau goes from -1 to 1, centered at zero
            tau = np.linspace(-1.0, 1.0, npts)

            # t is the time axis, in s
            xdata = np.linspace(0, duration, npts)

            # This is a constant, determines the smoothness of amplitude at ends
            beta = np.log((1 + np.sqrt(1-trunc_value**2)) / trunc_value)

            # The amplitude is F1
            F1 = 1/np.cosh(beta * tau**n_exp)

            # Not calculating phase in this implementation
            F2 = scipy.integrate.cumtrapz(F1**2) # has one less element than F1
            F2 = np.concatenate([[0], F2]) # Prepend a zero value

            # Calculate frequency sweep in Hz
            F2_range = F2.max() - F2.min()
            omega_Hz = F2 * BW / F2_range
            omega_Hz = omega_Hz - BW/2

            omega_radians_per_s = omega_Hz * 2 * math.pi
            phs_radians = scipy.integrate.cumtrapz(omega_radians_per_s * duration/(npts-1) )
            phs_radians = np.concatenate([[0], phs_radians]) # Prepend a zero value
        
            amp = F1
            phs = phs_radians


        except:
            print("HSn pulse error, param object contains: ", params)

    else:
        amp = np.array([2, 2, 2, 2])
        xdata = np.array([1, 2, 3, 4])
        phs = np.array([1, 2, 3, 4])

    xdata = format_numpy_as_json_list(xdata)
    amp = format_numpy_as_json_list(amp)
    phs = format_numpy_as_json_list(phs)

    return {
        # Note: if np thinks the arrays are floats it will call this formatter. 
        'xdata': xdata,
        'ydata': amp,
        'phase': phs
    }   

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
