from SignalModel import Signal
from ThresholdSelect import ThSelect
from ThresholdFunction import ThFuction
import numpy as np
import pywt
import matplotlib.pyplot as plt
from DenoiseResult import DenoiseRsult


def dwtdec(data, delevel=None):
    w = pywt.Wavelet('db4')
    if not delevel:
        maxlev = pywt.dwt_max_level(len(data), w.dec_len)
        delevel = maxlev
    coeffs = pywt.wavedec(data, 'db4', level=delevel)
    return coeffs


def thprocess(coeffs, thf='soft'):
    ncoeffs = [coeffs[0]]
    for i in range(1, len(coeffs)):
        th = ThSelect(coeffs[i]).DonohoThEx()
        if thf == 'soft':
            ncf = ThFuction(coeffs[i]).thsoft(th)
        elif thf == 'hard':
            ncf = ThFuction(coeffs[i]).thhard(th)
        ncoeffs.append(np.asarray(ncf))
    return ncoeffs


if __name__ == '__main__':
    s = Signal(1000)
    od1 = s.createSin(50, 60, 4)
    od2 = s.createPulse(50, 60, 4)
    od3 = s.createSpikes(4)
    ods = [od1, od2, od3]
    spds = []
    hpds = []
    for od in ods:
        coeffs = dwtdec(od, delevel=4)
        nscoeffs = thprocess(coeffs, thf='soft')
        nhcoeffs = thprocess(coeffs, thf='hard')
        spd = pywt.waverec(nscoeffs, 'db4')
        hpd = pywt.waverec(nhcoeffs, 'db4')
        spds.append(spd)
        hpds.append(hpd)

    ssnrs = []
    hsnrs = []
    smses = []
    hmses = []

    ssms = []
    hsms = []
    slrepvs = []
    hlrepvs = []
    tds = [s.createSin(50, 60, 0), s.createPulse(50, 60, 0), s.createSpikes(0)]
    for i in range(len(tds)):
        sdr = DenoiseRsult(tds[i], spds[i])
        hdr = DenoiseRsult(tds[i], hpds[i])
        ssnrs.append(sdr.snr())
        hsnrs.append(hdr.snr())
        smses.append(sdr.mse())
        hmses.append(hdr.mse())

        ssms.append(sdr.smooth(ods[i]))
        hsms.append(hdr.smooth(ods[i]))
        slrepvs.append(sdr.lrepv(ods[i], 32))
        hlrepvs.append(hdr.lrepv(ods[i], 32))
    print('ssnrs = {0}'.format(ssnrs))
    print('hsnrs = {0}'.format(hsnrs))
    print('smses = {0}'.format(smses))
    print('hmses = {0}'.format(hmses))
    print()
    print('ssms = {0}'.format(ssms))
    print('hsms= {0}'.format(hsms))
    print('slrepvs = {0}'.format(slrepvs))
    print('hlrepvs = {0}'.format(slrepvs))

    x = [x for x in range(1000)]
    plt.figure()
    plt.subplot(3, 2, 1)
    plt.plot(x, spds[0])
    plt.title("Sine signal by soft threshold")
    plt.subplot(3, 2, 2)
    plt.plot(x, hpds[0])
    plt.title("Sine signal by hard threshold")
    plt.subplot(3, 2, 3)
    plt.plot(x, spds[1])
    plt.title("Pulse signal by soft threshold")
    plt.subplot(3, 2, 4)
    plt.plot(x, hpds[1])
    plt.title("pulse signal by hard threshold")
    plt.subplot(3, 2, 5)
    plt.plot(x, spds[2])
    plt.title("Spike signal by soft threshold")
    plt.subplot(3, 2, 6)
    plt.plot(x, hpds[2])
    plt.title("Spike signal by hard threshold")
    plt.tight_layout()
    plt.show()

    l2spds = []
    l4spds = []
    l7spds = []
    for od in ods:
        coeffs = dwtdec(od, 2)
        nscfsl2 = thprocess(coeffs, thf='soft')
        spd = pywt.waverec(nscfsl2, 'db4')
        l2spds.append(spd)
    for od in ods:
        coeffs = dwtdec(od, 4)
        nscfsl4 = thprocess(coeffs, thf='soft')
        spd = pywt.waverec(nscfsl4, 'db4')
        l4spds.append(spd)
    for od in ods:
        coeffs = dwtdec(od)
        nscfsl4 = thprocess(coeffs, thf='soft')
        spd = pywt.waverec(nscfsl4, 'db4')
        l7spds.append(spd)

    plt.figure()
    plt.subplot(3, 1, 1)
    plt.title('Sine signal as decomposed level = 2')
    plt.plot(x, l2spds[0])
    plt.subplot(3, 1, 2)
    plt.title('Sine signal as decomposed level = 4')
    plt.plot(x, l4spds[0])
    plt.subplot(3, 1, 3)
    plt.title('Sine signal as decomposed level = 7')
    plt.plot(x, l7spds[0])
    plt.tight_layout()

    plt.figure()
    plt.subplot(3, 1, 1)
    plt.title('Pulse signal as decomposed level = 2')
    plt.plot(x, l2spds[1])
    plt.subplot(3, 1, 2)
    plt.title('Pulse signal as decomposed level = 4')
    plt.plot(x, l4spds[1])
    plt.subplot(3, 1, 3)
    plt.title('Pulse signal as decomposed level = 7')
    plt.plot(x, l7spds[1])
    plt.tight_layout()

    plt.figure()
    plt.subplot(3, 1, 1)
    plt.title('Spike signal as decomposed level = 2')
    plt.plot(x, l2spds[2])
    plt.subplot(3, 1, 2)
    plt.title('Spike signal as decomposed level = 4')
    plt.plot(x, l4spds[2])
    plt.subplot(3, 1, 3)
    plt.title('Spike signal as decomposed level = 7')
    plt.plot(x, l7spds[2])
    plt.tight_layout()
    plt.show()




