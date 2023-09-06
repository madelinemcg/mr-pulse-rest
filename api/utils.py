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
            # 20230905 PJB: fixed bug with non-integer n_exp. 
            #F1 = 1/np.cosh(beta * tau**n_exp)
            F1 = 1/np.cosh(beta * np.abs(tau)**n_exp)

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




########### SIMULATION CODE #######################
# This is a matrix version of a Bloch simulator using the 4th order Runge-Kutta
# ODE solver. This one simultaneously solves for an array of offset values.
# The magnetization M and its time derivative dMdt has shape [num_offsets, 3] 
# num_offsets = offsets.shape[0]. R1, R2, b1x, and b1y are all assumed scalars,
# although if they have the same shape as offsets it will also work.
# This adds an offset dimension ot the calculation but goes much faseter
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


# Hardcoded simulation. You need to pass the parameters in the INPUTS section below
def simulate_effect_of_rf_pulse():

    ################ INPUTS ################
    # Pass in the xdata, amp, and pha, same array values that are returned from graph_data()
    # These you will pack up in JSON and unpack here
    # I'm hardwiring a simple sinc here
    xdata = np.array([0.000, 0.133, 0.267, 0.400, 0.533, 0.667, 0.800, 0.933, 1.067, 1.200, 1.333, 1.467, 1.600, 1.733, 1.867, 2.000])
    phs = np.array([-0.000, -0.000, -0.000, -0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, -0.000, -0.000, -0.000, -0.000])
    amp = np.array([-0.000, -0.136, -0.216, -0.156, 0.071, 0.413, 0.757, 0.971, 0.971, 0.757, 0.413, 0.071, -0.156, -0.216, -0.136, -0.000])

    # These are scalar values that come from sliders. Pass these in too
    # Configure the sliders to give the min, max, step and default values specified below
    simulation_bw = 4000 # min 100, max 20000, setp 100, default4000
    offset_steps = 101 # min 30, max 1000, step 10, default 101
    gamma_b1_max = 353 # min 0, max 4000, step 5, default 353 
    pulse_phase = 0 # I would not add this to the GUI, don't even pass this in, leave hardwired to 0
    T1 = 2000 # min 50, max 10000, step 10, defualat 2000
    T2 = 100 # min 5, max 1000, step 5, default 100

    # Note this parameter is "duration" from the pulse shape GUI. You need to pass this in. 
    duration = 2
    ################ END INPUTS ################

    # These values are calculated from the input values above
    Tp = duration / 1000 # duration is in milliseconds, but the code below needs Tp as seconds
    t = xdata
    Npts = len(t)
    b1_amp = amp
    b1_phase = phs
    M0 = np.array([0, 0, 1.0]) # Initial magnetization

    # These are teh frequency offsets that will be plotted
    offsets = np.linspace(-simulation_bw/2, simulation_bw/2, offset_steps)

    # Convert polar RF into cartesian components
    b1x = 2 * np.pi * gamma_b1_max * b1_amp * np.cos(pulse_phase + b1_phase)
    b1y = 2 * np.pi * gamma_b1_max * b1_amp * np.sin(pulse_phase + b1_phase)

    Mt = np.zeros([offset_steps, Npts, 3])
    deltaTp = Tp / Npts

    # Array version of simulator
    Mt[:, 0, :] = M0

    # Loop over all time points 
    for tdx in range(1, Npts):
        Mt[:, tdx,:] = blochRK4_arrayform(Mt[:, tdx-1,:], b1x[tdx], b1y[tdx], offsets*2*np.pi, 1000/T1, 1000/T2, deltaTp)

    # Save the values at the end of the time pulse
    Mend = Mt[:,-1,:]

    Mxy = np.sqrt(Mend[:,0]**2 + Mend[:,1]**2)
    Mz = Mend[:,2]

    # Both Mxy and Mz are ydata values, but the share the same x-axis
    return {
        'xdata': offsets,
        'Mxy': Mxy,
        'Mz': Mz
    } 

