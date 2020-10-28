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
    cvthss = []
    gcvthss = []
    srmthss = []
    thsmatrix = [gthss, cvthss, gcvthss, srmthss]
    thmname = ['gth', 'cv', 'gcv', 'srm']
    thfname = ['soft', 'hard', 'thsemisf', 'thf1', 'thf2', 'thf3']
    gpds = []
    cvpds = []
    gcvpds = []
    srmpds = []
    pdsmatrix = [gpds, cvpds, gcvpds, srmpds]

    for od in ods:
        dwd = DWTP(od)
        coeffs = dwd.dwtdec(wtname='db4', delevel=4)
        gths = []
        cvths = []
        gcvths = []
        srmths = []
        for i in range(1, len(coeffs)):
            bthe = BestThEstimate(coeffs[i], thfunction=thfname[4], thp=4)
            thsa = ThSearchAlgorithm()
            gth = ThSelect(coeffs[i]).DonohoThEx()
            cvthhf = thsa.FibonacciSearch(bthe.cvalfunction, [0, 1.5*gth], 0.001)
            cvth = (1 + mt.log(2)/mt.log(len(coeffs[i])))**0.5*cvthhf
            gcvth = thsa.FibonacciSearch(bthe.gcvfunction, [0, 1.5*gth], 0.001)
            srmth = thsa.FibonacciSearch(bthe.msesurefuction, [0, 1.5*gth], 0.001)
            gths.append(gth)
            cvths.append(cvth)
            gcvths.append(gcvth)
            srmths.append(srmth)
        gthss.append(gths)
        cvthss.append(cvths)
        gcvthss.append(gcvths)
        srmthss.append(srmths)

    for i in range(len(thsmatrix)):
        for j in range(len(ods)):
            dwd = DWTP(ods[j])
            coeffs = dwd.dwtdec(wtname='db4', delevel=4)
            ths = thsmatrix[i]
            ncoeffs = dwd.thprocess(coeffs, ths=thsmatrix[i][j], thf=thfname[4], thp=4)
            pd = dwd.dwtrec(ncoeffs, wtname='db4')
            pdsmatrix[i].append(pd)

    ssnrs = []
    cvsnrs = []
    gcvsnrs = []
    srmsnrs = []

    smses = []
    cvmses = []
    gcvmses = []
    srmmses = []

    tds = [s.createSin(50, 60, 0), s.createPulse(50, 60, 0), s.createSpikes(0)]
    for i in range(len(tds)):
        sdr = DenoiseRsult(tds[i], gpds[i])
        cvdr = DenoiseRsult(tds[i], cvpds[i])
        gcvdr = DenoiseRsult(tds[i], gcvpds[i])
        srmdr = DenoiseRsult(tds[i], srmpds[i])

        ssnrs.append(sdr.snr())
        cvsnrs.append(cvdr.snr())
        gcvsnrs.append(gcvdr.snr())
        srmsnrs.append(srmdr.snr())

        smses.append(sdr.mse())
        cvmses.append(cvdr.mse())
        gcvmses.append(gcvdr.mse())
        srmmses.append(srmdr.mse())

    snrss = [ssnrs, cvsnrs, gcvsnrs, srmsnrs]
    snrsn = ['ssnrs', 'cvsnrs', 'gcvsnrs', 'srmsnrs']
    msess = [smses, cvmses, gcvmses, srmmses]
    msesn = ['smses', 'cvmses', 'gcvmses', 'srmmses']
    for i in range(len(snrss)):
        print('{0} = {1}'.format(snrsn[i], snrss[i]))
    print()
    for i in range(len(msess)):
        print('{0} = {1}'.format(msesn[i], msess[i]))
    x = [x for x in range(1000)]
    for j in range(len(ods)):
        plt.figure()
        for i in range(4):
            plt.subplot(2, 2, i+1)
            plt.title('{0} signal with {1} threshold'.format(dnames[j], thmname[i]))
            plt.plot(x, pdsmatrix[i][j])
        plt.tight_layout()
        plt.show()






