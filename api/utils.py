import numpy as np


# TODO: Redirects calculation based on pulse type
def graph_data(pulse_type):
    xdata = []
    ydata = []

    npts = 16 # very short! Typically >200
    duration = 2 # milliseconds

    # Calculate time axes. xdata is time, from 0 to duration.
    # Tau is normalized from -1 to 1
    tau = np.linspace(-1.0, 1.0, npts)
    xdata = np.linspace(0, duration, npts)

    print(f'pulse_type = {pulse_type}')

    if pulse_type == 'sinc':
        print("graph_data: in sinc")

        nlobes = 5
        ydata = np.sin((nlobes+1) * np.pi * tau ) / ((nlobes+1) * np.pi * tau)
        ydata[np.isnan(ydata)] = 1.0 # correct div by zero error

    elif pulse_type == 'gauss':
        print("graph_data: in gauss")

        # Here is the calculation of the guassian shape
        truncation_sigma = 3
        ydata = np.exp(-0.5 * (tau * truncation_sigma)**2)

    else:
        print("graph_data: no type defined")
        ydata = [4, 2, 1, 1]
        xdata = [1, 2, 3, 4]

    return {
        'xdata': str(xdata),
        'ydata': str(ydata)
    }
