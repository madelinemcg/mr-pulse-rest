import numpy as np

class PulseParam:
    def __init__(self, name, value, minimum, maximum, step):
        self.name = name
        self.value = value
        self.min = minimum
        self.max = maximum
        self.step = step

class Pulse:
    def __init__(self):
        self.title = "Choose Pulse"
        self.type = "NONE"
        self.createGraphFields()
        self.createSimFields()
        self.calculateGraph()
        self.calculateSim()

    def createGraphFields(self):
        self.graph_fields = []

    def createSimFields(self):
        bw = PulseParam("bw", 4000, 100, 10000, 100)
        offset = PulseParam("offset", 101, 30, 1000, 10)
        gamma_b1 = PulseParam("gamma b1", 353, 100, 1000, 5)
        phase = PulseParam("phase", 0, 0, 10, 1)
        t1 = PulseParam("t1", 1000, 100, 10000, 100) 
        t2 = PulseParam("t2", 1000, 100, 10000, 100) 
        self.sim_fields = [bw, offset, gamma_b1, phase, t1, t2]
    
    def calculateGraph(self):
        self.graph_data = []

    def calculateSim(self):
        self.sim_data = []

class Sinc (Pulse):
    def __init__(self):
        self.title = "Windowed Sinc"
        self.type = "SINC"
        self.createGraphFields()
        self.createSimFields()
        self.calculateGraph()
        self.calculateSim()

    def createGraphFields(self):
        duration = PulseParam("duration", 2, 0.1, 20, 0.1)
        ntps = PulseParam("ntps", 128, 32, 512, 16)
        nlobes = PulseParam("nlobes", 128, 32, 512, 16)
        window_a = PulseParam("window alpha", 128, 32, 512, 16)
        self.graph_fields = [duration, ntps, nlobes, window_a]

    def calculateGraph(self):
        self.graph_data = [1, 2, 3, 4, 5]

    def calculateSim(self):
        self.sim_data = [1, 2, 3, 4, 5]

