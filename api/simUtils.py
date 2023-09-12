from baseUtils import format_numpy_as_json_list
import numpy as np
import json

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
def simulate_effect_of_rf_pulse(pulse_type, graph_data, graph_params, sim_params):
    if pulse_type == 'none':
        xdata = np.array([1, 2, 3, 4])
        Mxy = np.array([2, 2, 2, 2])
        Mz = np.array([1, 1, 1, 1])

        xdata = format_numpy_as_json_list(xdata)
        Mxy = format_numpy_as_json_list(Mxy)
        Mz = format_numpy_as_json_list(Mz)

        # Both Mxy and Mz are ydata values, but the share the same x-axis
        return {
            'xdata': xdata,
            'mxy': Mxy,
            'mz': Mz
        } 
    
    graph_params = json.loads(graph_params)
    sim_params = json.loads(sim_params)

    ################ INPUTS ################
    # Pass in the xdata, amp (ydata), and pha (phase), same array values that are returned from graph_data()
    # These you will pack up in JSON and unpack here
    #xdata = graph_data["xdata"]
    xdata = json.loads(graph_data["xdata"])
    phs = json.loads(graph_data["phase"])
    amp = json.loads(graph_data["ydata"])
    xdata = np.array(xdata)
    phs = np.array(phs)
    amp = np.array(amp)

    # These are scalar values that come from sliders. Pass these in too
    # Configure the sliders to give the min, max, step and default values specified below
    for pulse_dict in sim_params:
        if pulse_dict["name"] == "simulation bw":
            simulation_bw = pulse_dict["val"]
        elif pulse_dict["name"] == "offset steps":
            offset_steps = pulse_dict["val"]
        elif pulse_dict["name"] == "gamma b1 max":
            gamma_b1_max = pulse_dict["val"]
        elif pulse_dict["name"] == "T1":
            T1 = pulse_dict["val"]
        elif pulse_dict["name"] == "T2":
            T2 = pulse_dict["val"]

    # simulation_bw = 4000 # min 100, max 20000, setp 100, default4000
    # offset_steps = 101 # min 30, max 1000, step 10, default 101
    # gamma_b1_max = 353 # min 0, max 4000, step 5, default 353 
    pulse_phase = 0 # I would not add this to the GUI, don't even pass this in, leave hardwired to 0
    # T1 = 2000 # min 50, max 10000, step 10, defualat 2000
    # T2 = 100 # min 5, max 1000, step 5, default 100

    # Note this parameter is "duration" from the pulse shape GUI. You need to pass this in. 
    for pulse_dict in graph_params:
        if pulse_dict["name"] == "duration":
            duration = pulse_dict["val"]
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

    offsets = format_numpy_as_json_list(offsets)
    Mxy = format_numpy_as_json_list(Mxy)
    Mz = format_numpy_as_json_list(Mz)

    # Both Mxy and Mz are ydata values, but the share the same x-axis
    return {
        'xdata': offsets,
        'mxy': Mxy,
        'mz': Mz
    } 
