from SignalModel import Signal
import matplotlib.pyplot as plt
from WtProcess import SWTP
from SpatialCorrelationThresholdALG import SpCoThALG
from ThSearchAlgorithm import ThSearchAlgorithm
from ThresholdSelect import ThSelect

if __name__ == '__main__':
    s = Signal(1024)
    od1 = s.createSin(50, 60, 4)
    od2 = s.createPulse(50, 60, 4)
    od3 = s.createSpikes(4)
    ods = [od1, od2, od3]
    dnames = ['Sine', 'Pulse', 'Spike']
    sfp1pds = []
    sfp2pds = []
    for od in ods:
        swt = SWTP(od)
        coeffs = swt.swtdec(delevel=4)
        spta2 = SpCoThALG(coeffs)
        sfp1gcvs = []
        sfp2gcvs = []
        P = spta2.spcoCors()
        spta2.BTHassitIndex(1, pk=0.1, pa=4, mode='srmse')
        for k in range(1, 100):
            sfp2gcv = spta2.BTHspcothfwp2(k/10)
            sfp2gcvs.append(sfp2gcv)
        x=[x/10 for x in range(1, 100)]
        plt.figure()
        plt.plot(x, sfp2gcvs)
    plt.show()
