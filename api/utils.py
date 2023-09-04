import numpy as np
import scipy.integrate as integrate
import json
import math

# Converts numpy array to JSON-friendly (adds commas between values)
def format_numpy_as_json_list(array):
        astring = '['
        for element in array:
            astring += f'{element:.3f}, '
               
        # Now chop off that last space and comma before ending
        astring = astring[0:-2]    
        astring += ']'
        return astring

def dM_dt_function_arrayform(b1x, b1y, R1, R2, offsets, M):
  dMdt = np.zeros([offsets.shape[0], 3])
  #dMdt = M * 0 # Initize the 3D vector

  # The three components of dM/dt:
  dMdt[:,0] = offsets * M[:,1] - (b1y * M[:,2]) - (M[:,0] * R2)
  dMdt[:,1] = b1x * M[:,2] - (offsets * M[:,0]) - (M[:,1] * R2)
  dMdt[:,2] = b1y * M[:,0] - (b1x * M[:,1] + ((1.0 - M[:,2]) * R1))

  return dMdt

def blochRK4_arrayform(Minit, B1x, B1y, offsets, R1, R2, deltaT):
  # temp variable holding output of each of 4 iterations
  KK = np.zeros([4, offsets.shape[0], 3]) # 4 iterations, each holding a 4D vector [num_offsets, Mx, My, Mz]

  KK[0,:,:] = deltaT * dM_dt_function_arrayform(B1x, B1y, R1, R2, offsets, Minit)
  KK[1,:,:] = deltaT * dM_dt_function_arrayform(B1x, B1y, R1, R2, offsets, Minit + KK[0,:,:]/2)
  KK[2,:,:] = deltaT * dM_dt_function_arrayform(B1x, B1y, R1, R2, offsets, Minit + KK[1,:,:]/2)
  KK[3,:,:] = deltaT * dM_dt_function_arrayform(B1x, B1y, R1, R2, offsets, Minit + KK[2,:,:])

  # Take weighted sum of all K values
  Mnext = Minit + 1/6 * (KK[0,:] + 2*KK[1,:] + 2*KK[2,:] + KK[3,:] )

  return Mnext

# Redirects calculation based on pulse type
def graph_data(pulse_type, params):
    xdata = np.empty([0, 0], dtype=float)
    ydata = np.empty([0, 0], dtype=float)

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

            ydata = np.sin((nlobes+1) * np.pi * tau ) / ((nlobes+1) * np.pi * tau)
            ydata[np.isnan(ydata)] = 1.0 # correct div by zero error
            
            if window_alpha<1.0:
                window_function = window_alpha + (1-window_alpha) * np.cos(2 * np.pi * tau)
                ydata = ydata * window_function


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

            ydata = np.exp(-0.5 * (tau * truncation_sigma)**2)
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
            ydata = xdata*0 + 1.

            # It is slightly inexact to set the endpoints to zero, but it shows 
            # the pulse shape better.
            ydata[0] = 0.0
            ydata[-1] = 0.0

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
            ydata = 1/np.cosh(beta * tau**n_exp)

            '''
            # Not calculating phase in this implementation
            F2 = integrate.cumtrapz(F1**2) # has one less element than F1
            F2 = np.concatenate([[0], F2]) # Prepend a zero value
            # Calculate frequency sweep in Hz
            F2_range = F2.max() - F2.min()
            omega_Hz = F2 * BW / F2_range
            omega_Hz = omega_Hz - BW/2
            if not freq_sweep:
                omega_Hz = omega_Hz * -1

            omega_radians_per_s = omega_Hz * 2 * math.pi
            phs_radians = integrate.cumtrapz(omega_radians_per_s * pulse_duration/(npts-1) )
            phs_radians = np.concatenate([[0], phs_radians]) # Prepend a zero value
            '''

            ydata = np.exp(-0.5 * (tau * trunc_value)**2)

        except:
            print("HSn pulse error, param object contains: ", params)

    else:
        ydata = np.array([2, 2, 2, 2])
        xdata = np.array([1, 2, 3, 4])

    xdata = format_numpy_as_json_list(xdata)
    ydata = format_numpy_as_json_list(ydata)

    return {
        # Note: if np thinks the arrays are floats it will call this formatter. 
        'xdata': xdata,
        'ydata': ydata
    }   

def sim_data(pulse_type, graph_params, sim_params):
    xdata = np.empty([0, 0], dtype=float)
    ydata = np.empty([0, 0], dtype=float)

    graph_params = json.loads(graph_params)
    sim_params = json.loads(sim_params)

    # Needs from graph_params: calculate t, b1_amp, b1_phase
    # Meaning: npts, duration, truncation_sigma?, 
    if pulse_type != 'none':
        try:
            for sim_dict in sim_params:
                if sim_dict["name"] == "simulation bw":
                    sim_bw = sim_dict["val"]
                elif sim_dict["name"] == "offset steps":
                    offset_steps = sim_dict["val"]
                elif sim_dict["name"] == "gamma b1 max":
                    b1_max = sim_dict["val"]
                elif sim_dict["name"] == "phase":
                    phase = sim_dict["val"]
                elif sim_dict["name"] == "T1":
                    T1 = sim_dict["val"]
                elif sim_dict["name"] == "T2":
                    T2 = sim_dict["val"]

            if pulse_type == 'sinc':
                for pulse_dict in graph_params:
                    if pulse_dict["name"] == "npts":
                        npts = pulse_dict["val"]
                    elif pulse_dict["name"] == "duration":
                        duration = pulse_dict["val"]
                    elif pulse_dict["name"] == "nlobes":
                        nlobes = pulse_dict["val"]
                    elif pulse_dict["name"] == "window alpha":
                        window_alpha = pulse_dict["val"]

                tau = np.linspace(-0.5, 0.5, npts)
                amp = np.sin((nlobes + 1) * np.pi * tau) / ((nlobes + 1) * np.pi * tau)

                if window_alpha < 1.0:
                    window_function = window_alpha + (1-window_alpha) * np.cos(2 * np.pi * tau)
                    amp = amp * window_function
                
                amp[np.isnan(amp)] = 1.0

                t = np.linspace(0, duration, npts)
                b1_amp = amp
                b1_phase = amp * 0
            
            elif pulse_type == 'gauss':
                for pulse_dict in graph_params:
                    if pulse_dict["name"] == "npts":
                        npts = pulse_dict["val"]
                    elif pulse_dict["name"] == "duration":
                        duration = pulse_dict["val"]
                    elif pulse_dict["name"] == "trunc":
                        truncation_sigma = pulse_dict["val"]

                tau = np.linspace(-1.0, 1.0, npts)
                amp = np.exp(-0.5 * (tau * truncation_sigma)**2)

                t = np.linspace(0, duration, npts)
                b1_amp = amp
                b1_phase = amp * 0

            if pulse_type == 'square':
                for pulse_dict in graph_params:
                    if pulse_dict["name"] == "npts":
                        npts = pulse_dict["val"]
                    elif pulse_dict["name"] == "duration":
                        duration = pulse_dict["val"]

                t = np.linspace(0, duration, npts)
                amp = t*0 + 1.0

                b1_amp = amp
                b1_phase = amp * 0

            elif pulse_type == 'HSn':
                for pulse_dict in graph_params:
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

                BW = r_value / duration
                tau = np.linspace(-1.0, 1.0, npts)

                # This is a constant, determines the smoothness of amplitude at ends
                beta = np.log((1 + np.sqrt(1-trunc_value**2)) / trunc_value)

                # THe amplitude is F1
                F1 = 1/np.cosh(beta * tau**n_exp)
                F2 = integrate.cumtrapz(F1**2) # has one less element than F1
                F2 = np.concatenate([[0], F2]) # Prepend a zero value

                # Calculate frequency sweep in Hz
                F2_range = F2.max() - F2.min()
                omega_Hz = F2 * BW / F2_range
                omega_Hz = omega_Hz - BW/2

                omega_radians_per_s = omega_Hz * 2 * math.pi

                phs_radians = integrate.cumtrapz(omega_radians_per_s * duration/(npts-1) )
                phs_radians = np.concatenate([[0], phs_radians])

                t = np.linspace(0, duration, npts)
                b1_amp = F1
                b1_phase = phs_radians
            
            tp = duration / 1000
            M0 = np.array([0, 0, 1.0])

            offsets = np.linspace(-sim_bw/2, sim_bw/2, offset_steps)

            b1x = 2 * np.pi * b1_max * b1_amp * np.cos(phase + b1_phase)
            b1y = 2 * np.pi * b1_max * b1_amp * np.sin(phase + b1_phase)

            Mt = np.zeros([offset_steps, npts, 3])
            deltaTp = tp / npts

            Mt[:, 0, :] = M0

            for tdx in range(1, npts):
                Mt[:, tdx,:] = blochRK4_arrayform(Mt[:, tdx-1,:], b1x[tdx], b1y[tdx], offsets*2*np.pi, 1/T1, 1/T2, deltaTp)

            Mend = Mt[:,-1,:]
            Mxy = np.sqrt(Mend[:,0]**2 + Mend[:,1]**2)
            Mz = Mend[:,2]

        except:
            print("Simulation Error - params are: ", sim_params)

    else:
        ydata = np.array([2, 2, 2, 2])
        xdata = np.array([1, 2, 3, 4])

    xdata = format_numpy_as_json_list(xdata)
    ydata = format_numpy_as_json_list(ydata)

    return {
        'xdata': xdata,
        'ydata': ydata
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

def base_sim_params(pulse_type):
    params = json.dumps([])

    if pulse_type != 'none':
        params = json.dumps([{"name": "simulation bw", "val": 4000, "min": 100, "max": 10000, "step": 100},
                             {"name": "offset steps", "val": 101, "min": 30, "max": 1000, "step": 10},
                             {"name": "gamma b1 max", "val": 353, "min": 30, "max": 1000, "step": 5},
                             {"name": "phase", "val": 0, "min": 0, "max": 10, "step": 1},
                             {"name": "T1", "val": 1000, "min": 100, "max": 10000, "step": 100},
                             {"name": "T2", "val": 1000, "min": 100, "max": 10000, "step": 100},
                             ])

    return params
