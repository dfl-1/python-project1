from SignalModel import Signal
from LayerSelect import LayerSelect
import matplotlib.pyplot as plt
import numpy as np
from BlockThMethod import BlockThMethod
from ThresholdSelect import ThSelect
from WtProcess import SWTP
from DenoiseResult import DenoiseRsult

if __name__ == '__main__':
    s = Signal(1024)
    od1 = s.createSin(50, 60, 4)
    od2 = s.createPulse(50, 60, 4)
    od3 = s.createSpikes(4)
    ods = [od1, od2, od3]
    spds = []
    hpds = []
    thsemispds = []
    thf1pds = []
    thf2pds = []
    thf3pds = []
    dnames = ['Sine', 'Pulse', 'Spike']
    thfname = ['soft', 'hard', 'thf3']
    pdsmatrix = [spds, hpds, thf3pds]
    thps = [None, None, 2]

    for od in ods:
        swt = SWTP(od)
        dl = swt.maxdeclevel()
        coeffs = swt.swtdec(wtname='db4', delevel=4)
        for i in range(len(pdsmatrix)):
            ncoeffs = swt.thprocess(coeffs, thf=thfname[i], thp=thps[i])
            pd = swt.swtrec(ncoeffs, wtname='db4')
            pdsmatrix[i].append(pd)

    x = [x for x in range(1024)]
    for j in range(3):
        plt.figure()
        plt.subplot(2, 2, 1)
        plt.title('Noisy {0} signal '.format(dnames[j]))
        plt.plot(x, ods[j])

        plt.subplot(2, 2, 2)
        plt.title('{0} signal by {1} threshold(SWT)'.format(dnames[j], thfname[0]))
        plt.plot(x, pdsmatrix[0][j])

        plt.subplot(2, 2, 3)
        plt.title('{0} signal by {1} threshold(SWT)'.format(dnames[j], thfname[1]))
        plt.plot(x, pdsmatrix[0][j])

        plt.subplot(2, 2, 4)
        plt.title('{0} signal by {1} threshold(SWT)'.format(dnames[j], thfname[2]))
        plt.plot(x, pdsmatrix[0][j])
        plt.tight_layout()
        plt.show()