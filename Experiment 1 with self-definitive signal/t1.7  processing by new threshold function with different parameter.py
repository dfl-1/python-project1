from SignalModel import Signal
from LayerSelect import LayerSelect
import matplotlib.pyplot as plt
import numpy as np
import math as mt
from BlockThMethod import BlockThMethod
from ThresholdSelect import ThSelect
from BestThEstimation import BestThEstimate
from ThSearchAlgorithm import ThSearchAlgorithm
from WtProcess import DWTP
from DenoiseResult import DenoiseRsult

if __name__ == '__main__':
    s = Signal(1000)
    od1 = s.createSin(50, 60, 4)
    od2 = s.createPulse(50, 60, 4)
    od3 = s.createSpikes(4)
    ods = [od1, od2, od3]
    dnames = ['Sine', 'Pulse', 'Spike']
    gthss = []
    bsthss = []
    gthpds = []
    bsthpds =[]
    dl = 4
    for od in ods:
        dwd = DWTP(od)
        coeffs = dwd.dwtdec(wtname='db4', delevel=dl)
        gths = []
        bsths = []
        for i in range(1, len(coeffs)):
            bthe = BestThEstimate(coeffs[i], thfunction='thf3', thp=2+2*i)
            thsa = ThSearchAlgorithm()
            gth = ThSelect(coeffs[i]).DonohoThEx()
            bsth = thsa.FibonacciSearch(bthe.msesurefuction, [0, 1.5 * gth], 0.001)
            gths.append(gth)
            bsths.append(bsth)
        gthss.append(gths)
        bsthss.append(bsths)

    for i in range(len(ods)):
        dwd = DWTP(ods[i])
        coeffs = dwd.dwtdec(wtname='db4', delevel=dl)
        gths = gthss[i]
        bsths = gthss[i]
        ncoeffs1 = dwd.thprocess2(coeffs, ths=gths, thf='thf3', thps=[2+2*k for k in range(dl)])
        ncoeffs2 = dwd.thprocess2(coeffs, ths=bsths, thf='thf3', thps=[2+2*k for k in range(dl)])
        gthpd = dwd.dwtrec(ncoeffs1, wtname='db4')
        bsthpd = dwd.dwtrec(ncoeffs2, wtname='db4')
        gthpds.append(gthpd)
        bsthpds.append(bsthpd)

    gthsnrs = []
    bsthsnrs = []
    gthmses = []
    bsthmses = []
    tds = [s.createSin(50, 60, 0), s.createPulse(50, 60, 0), s.createSpikes(0)]
    for i in range(len(tds)):
        gthdr = DenoiseRsult(tds[i], gthpds[i])
        bsthdr = DenoiseRsult(tds[i], bsthpds[i])
        gthsnrs.append(gthdr.snr())
        bsthsnrs.append(bsthdr.snr())
        gthmses.append(gthdr.mse())
        bsthmses.append(bsthdr.mse())
    print('gthsnrs = {0}'.format(gthsnrs))
    print('bsthsnrs = {0}'.format(bsthsnrs))
    print('gthmses = {0}'.format(gthmses))
    print('bsthmses = {0}'.format(bsthmses))

    x = [x for x in range(1000)]
    plt.figure()
    for i in range(len(ods)):
        plt.subplot(3, 2, 2 * i + 1)
        plt.title('{0} signal processed by gth'.format(dnames[i]))
        plt.plot(x, gthpds[i])
        plt.subplot(3, 2, 2 * i + 2)
        plt.title('{0} signal processed by bsth'.format(dnames[i]))
        plt.plot(x, bsthpds[i])
    plt.tight_layout()
    plt.show()