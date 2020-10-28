from SignalModel import Signal
from LayerSelect import LayerSelect
import matplotlib.pyplot as plt
import numpy as np
import math as mt
from BlockThMethod import BlockThMethod
from ThresholdSelect import ThSelect
from ThresholdFunction import ThFuction
from BestThEstimation import BestThEstimate
from ThSearchAlgorithm import ThSearchAlgorithm
from DenoiseResult import DenoiseRsult
from WtProcess import DWTP

if __name__ == '__main__':
    s = Signal(1000)
    od1 = s.createSin(50, 60, 4)
    od2 = s.createPulse(50, 60, 4)
    od3 = s.createSpikes(4)
    ods = [od1, od2, od3]
    td1 = s.createSin(50, 60, 0)
    td2 = s.createPulse(50, 60, 0)
    td3 = s.createSpikes(0)
    tds = [td1, td2, td3]
    for i in range(len(ods)):
        dwd = DWTP(ods[i])
        dwtd = DWTP(tds[i])
        coeffs = dwd.dwtdec(wtname='db4', delevel=4)
        tcoeffs = dwtd.dwtdec(wtname='db4', delevel=4)
        gcvths = []
        srmths = []
        mses = []
        bthe = BestThEstimate(coeffs[2], thfunction='thf3', thp=4)
        for k in range(1, 100):
            gcvth = bthe.gcvfunction(k/10)
            srmth = bthe.msesurefuction(k/10)
            thc = ThFuction(coeffs[2]).thf3(k/10, 4)
            mse = DenoiseRsult(tcoeffs[2], thc).mse()
            gcvths.append(gcvth)
            srmths.append(srmth)
            mses.append(mse)
        x = [x / 10 for x in range(1, 100)]
        plt.figure()
        l1, = plt.plot(x, [y+1 for y in srmths/np.max([abs(x) for x in srmths])], linestyle='-')
        l2, = plt.plot(x, mses/np.max(mses), linestyle='solid')
        plt.legend(handles=[l1, l2], labels=['Sure estimation', 'MSE'])
    plt.show()