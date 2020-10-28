import math as mt
import numpy as np


class AcSNR:
    def __init__(self, data, start,end):
        self.data = data
        self.start = start
        self.end = end

    def result(self,nstart, nend):
        sdn = np.std(self.data[nstart:nend])
        signal = np.max(self.data[self.start:self.end])
        snr = abs(signal/sdn)
        return snr










