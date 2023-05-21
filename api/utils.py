
# TODO: Redirects calculation based on pulse type
def graph_data(pulse_type):
    xdata = []
    ydata = []

    if pulse_type == 'sinc':
        print("graph_data: in sinc")
        ydata = [4, 2, 1]
        xdata = [1, 2, 3]

    elif pulse_type == 'gauss':
        print("graph_data: in gauss")
        ydata = [5, 3, 7]
        xdata = [1, 2, 3]

    return {
        'xdata': str(xdata),
        'ydata': str(ydata)
    }
