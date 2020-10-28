from SignalModel import Signal
from LayerSelect import LayerSelect
import matplotlib.pyplot as plt
import numpy as np
from BlockThMethod import BlockThMethod
from WtProcess import DWTP
from DenoiseResult import DenoiseRsult

if __name__ == '__main__':
    s = Signal(1000)
    od1 = s.createSin(50, 60, 4)
    od2 = s.createPulse(50, 60, 4)
    od3 = s.createSpikes(4)
    ods = [od1, od2, od3]
    spds = []
    blpds = []
    for od in ods:
        coeffs = DWTP(od).dwtdec(wtname='db4', delevel=3)
        nscoeffs = DWTP(od).thprocess(coeffs, thf='soft')
        spd = DWTP(od).dwtrec(nscoeffs, 'db4')
        spds.append(spd)

        nbcoeffs = [coeffs[0]]
        for j in range(1, len(coeffs)):
            bces = BlockThMethod(coeffs[j]).dividedblock()
            bceths = BlockThMethod(coeffs[j]).blockths()
            bces.insert(0, [0])  # 使系数列表与阈值列表相匹配
            a = len(bces)
            b = len(bceths)
            nbces = DWTP(od).thprocess(bces, ths=bceths, thf='soft')
            nbcoeff = BlockThMethod(coeffs[j]).recoverdata(nbces[1:])  # 除去添加的[0]系数
            nbcoeffs.append(np.asarray(nbcoeff))

        blpd = DWTP(od).dwtrec(nbcoeffs, 'db4')
        blpds.append(blpd)

    ssnrs = []
    blsnrs = []
    smses = []
    blmses = []
    tds = [s.createSin(50, 60, 0), s.createPulse(50, 60, 0), s.createSpikes(0)]
    for i in range(len(tds)):
        sdr = DenoiseRsult(tds[i], spds[i])
        bldr = DenoiseRsult(tds[i], blpds[i])
        ssnrs.append(sdr.snr())
        blsnrs.append(bldr.snr())
        smses.append(sdr.mse())
        blmses.append(bldr.mse())
    print('ssnrs = {0}'.format(ssnrs))
    print('blsnrs = {0}'.format(blsnrs))
    print('smses = {0}'.format(smses))
    print('blmses = {0}'.format(blmses))

    x = [x for x in range(1000)]
    plt.figure()
    plt.subplot(3, 2, 1)
    plt.title('Sine signal processed by soft threshold')
    plt.plot(x, spds[0])
    plt.subplot(3, 2, 2)
    plt.title('Sine signal processed by BP method')
    plt.plot(x, blpds[0])

    plt.subplot(3, 2, 3)
    plt.title('Pulse signal processed by soft threshold')
    plt.plot(x, spds[1])
    plt.subplot(3, 2, 4)
    plt.title('Pulse signal processed by BP method')
    plt.plot(x, blpds[1])

    plt.subplot(3, 2, 5)
    plt.title('Sine signal processed by soft threshold')
    plt.plot(x, spds[2])
    plt.subplot(3, 2, 6)
    plt.title('Sine signal processed by BP method')
    plt.plot(x, blpds[2])

    plt.tight_layout()
    plt.show()
