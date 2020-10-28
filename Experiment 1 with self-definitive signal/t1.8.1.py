from SignalModel import Signal
from LayerSelect import LayerSelect
import matplotlib.pyplot as plt
import numpy as np
import math as mt
from BlockThMethod import BlockThMethod
from ThresholdSelect import ThSelect
from BestThEstimation import BestThEstimate
from ThSearchAlgorithm import ThSearchAlgorithm
from WtProcess import SWTP
from DenoiseResult import DenoiseRsult

if __name__ == '__main__':
    s = Signal(4000)
    od1 = s.createSin(200, 60, 10)
    od2 = s.createPulse(200, 60, 10)
    od3 = s.createSpikes(10)
    ods = [od1, od2, od3]
    dnames = ['Sine', 'Pulse', 'Spike']
    gthss = []
    srmthss = []
    srmthss2 = []
    thsmatrix = [gthss, gthss, srmthss, srmthss2]
    thmname = ['sth', 'hth', 'srm', 'srm']
    thfname = ['soft', 'hard', 'thf3', 'thf3wp']
    spds = []
    hpds = []
    thf3pds = []
    thf3wppds = []
    pdsmatrix = [spds, hpds, thf3pds, thf3wppds]
    dl = 5

    for od in ods:
        swd = SWTP(od)
        coeffs = swd.swtdec(wtname='sym6', delevel=dl)
        gths = []
        gcvths = []
        srmths = []
        srmths2 = []
        for i in range(1, len(coeffs)):
            bthe = BestThEstimate(coeffs[i], thfunction='thf3', thp=4)
            bthe2 = BestThEstimate(coeffs[i], thfunction='thf3', thp=2 + 2 * i)
            thsa = ThSearchAlgorithm()
            gth = ThSelect(coeffs[i]).DonohoThEx()
            srmth = thsa.FibonacciSearch(bthe.msesurefuction, [0, 1*gth], 0.01)
            srmth2 = thsa.FibonacciSearch(bthe.msesurefuction, [0, 1*gth], 0.01)
            gths.append(gth)
            srmths.append(srmth)
            srmths2.append(srmth2)
        gthss.append(gths)
        srmthss.append(srmths)
        srmthss2.append(srmths2)

    for i in range(len(thsmatrix)):
        for j in range(len(ods)):
            swd = SWTP(ods[j])
            coeffs = swd.swtdec(wtname='sym6', delevel=dl)
            ths = thsmatrix[i]
            if i == 3:
                ncoeffs = swd.thprocess2(coeffs, ths=thsmatrix[i][j], thf='thf3', thps=[2 + 2 * k for k in range(dl)])
            else:
                ncoeffs = swd.thprocess(coeffs, ths=thsmatrix[i][j], thf=thfname[i], thp=4)
            pd = swd.swtrec(ncoeffs, wtname='sym6')
            pdsmatrix[i].append(pd)

    ssnrs = []
    hsnrs = []
    thf3snrs = []
    thf3wpsnrs = []

    smses = []
    hmses = []
    thf3mses = []
    thf3wpmses = []

    tds = [s.createSin(200, 60, 0), s.createPulse(200, 60, 0), s.createSpikes(0)]
    for i in range(len(tds)):
        sdr = DenoiseRsult(tds[i], spds[i])
        hdr = DenoiseRsult(tds[i], hpds[i])
        thf3dr = DenoiseRsult(tds[i], thf3pds[i])
        thf3wpdr = DenoiseRsult(tds[i], thf3wppds[i])

        ssnrs.append(sdr.snr())
        hsnrs.append(hdr.snr())
        thf3snrs.append(thf3dr.snr())
        thf3wpsnrs.append(thf3wpdr.snr())

        smses.append(sdr.mse())
        hmses.append(hdr.mse())
        thf3mses.append(thf3dr.mse())
        thf3wpmses.append(thf3wpdr.mse())

    snrss = [ssnrs, hsnrs, thf3snrs, thf3wpsnrs]
    snrsn = ['ssnrs', 'hsnrs', 'thf3snrs', 'thf3wpsnrs']
    msess = [smses, hmses, thf3mses, thf3wpmses]
    msesn = ['smses', 'hmses', 'thf3mses', 'thf3wpmses']
    for i in range(len(snrss)):
        print('{0} = {1}'.format(snrsn[i], snrss[i]))
    print()
    for i in range(len(msess)):
        print('{0} = {1}'.format(msesn[i], msess[i]))
    x = [x for x in range(4000)]
    for j in range(len(ods)):
        plt.figure()
        for i in range(4):
            plt.subplot(2, 2, i+1)
            plt.title('{0} signal with {1} threshold'.format(dnames[j], thmname[i]))
            plt.plot(x, pdsmatrix[i][j])
        plt.tight_layout()
        plt.show()