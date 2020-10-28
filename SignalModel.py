import numpy as np
import math as mt
import matplotlib.pyplot as plt


class Signal:
    def __init__(self, lens):
        self.lens = lens
        self.S = None
        self.N = None

    def createSin(self, fy, ra, Noisesize):
        t = np.arange(0, self.lens)
        y = ra * np.sin(t / fy)
        self.S = y
        n = np.random.rand(self.lens) * Noisesize
        self.N = n
        r = y + n
        return r

    def createPulse(self, fy, ra, Noisesize):
        t = np.arange(0, self.lens)
        y = np.sin(t / fy)
        y1 = y > 0
        self.S = ra * y1
        n = np.random.rand(self.lens) * Noisesize
        self.N = n
        r = ra * y1 + n
        return r

    def createSpikes(self, Noisesize):
        x = np.arange(0, self.lens)
        y = np.arange(0, self.lens)
        for t in x:
            y[t] = 15.6676 * (mt.exp(-0.0005 * (t - 230) ** 2) + 2 * mt.exp(-0.002 * (t - 330) ** 2) + 4 * mt.exp(
                -0.008 * (t - 470) ** 2) + 3 * mt.exp(-0.016 * (t - 690) ** 2) + mt.exp(-0.032 * (t - 830) ** 2))
        self.S = y
        n = np.random.rand(self.lens) * Noisesize
        self.N = n
        r = y + n
        return r

    def createSpikeMultiNoise(self, NoiseList):
        x = np.arange(0, self.lens)
        y = np.arange(0, self.lens)
        for t in x:
            y[t] = 15.6676 * (mt.exp(-0.0005 * (t - 230) ** 2) + 2 * mt.exp(-0.002 * (t - 330) ** 2) + 4 * mt.exp(
                -0.008 * (t - 470) ** 2) + 3 * mt.exp(-0.016 * (t - 690) ** 2) + mt.exp(-0.032 * (t - 830) ** 2))
        self.S = y
        nl = len(NoiseList)
        iy = self.lens//nl
        self.N = []
        r = []
        for i in range(nl-1):
            n = np.random.rand(iy)*NoiseList[i]
            self.N.extend(n)
            ir = y[i*iy:iy*(i+1)] + n
            r.extend(ir)
        n = np.random.rand(self.lens-(nl-1)*iy)*NoiseList[nl-1]
        self.N.extend(n)
        lr = y[(nl-1)*iy:] + n
        r.extend(lr)
        return r

    def getSNR(self):
        P_s = np.sum(abs(self.S) ** 2)
        P_n = np.sum(abs(self.N) ** 2)
        SNR = 10 * np.log10(P_s / P_n)
        return SNR


if __name__ == '__main__':
    t1 = Signal(1000)
    s = t1.createSpikes(0)
    s2 = t1.createSpikeMultiNoise([2,4,6])
    #print(t1.getSNR())
    plt.subplot(2, 1, 1)
    plt.plot([i for i in range(0, 1000)], s)
    plt.subplot(2, 1, 2)
    plt.plot([i for i in range(0, 1000)], s2)
    plt.show()
