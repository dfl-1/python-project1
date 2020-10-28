from GetActualSignal import GetActualSignal
from ThresholdSelect import ThSelect
from ThresholdFunction import ThFuction
import numpy as np
import pywt
import matplotlib.pyplot as plt
from DenoiseResult import DenoiseRsult
from WtProcess import DWTP
from AcSNR import AcSNR

if __name__ == '__main__':
    ad = GetActualSignal()
    ad.getwhvalue()
    od1 = ad.selectvalue(start=0, end=23552)
    dwt = DWTP(od1)
    coeffs = dwt.dwtdec(wtname='db4', delevel=4)
    nscoeffs = dwt.thprocess(coeffs, thf='soft')
    nhcoeffs = dwt.thprocess(coeffs, thf='hard')
    spd = dwt.dwtrec(nscoeffs, wtname='db4')
    hpd = dwt.dwtrec(nhcoeffs, wtname='db4')
    ad.outputdata(startidex=0, ogdata=od1, pddata=spd)

    ssm = DenoiseRsult([], spd).smooth(od1)
    hsm = DenoiseRsult([], hpd).smooth(od1)
    slrepv = DenoiseRsult([], spd).lrepv(od1, 128)
    hlrepv = DenoiseRsult([], hpd).lrepv(od1, 128)

    print('ssm = {0}'.format(ssm))
    print('hsm = {0}'.format(hsm))
    print('slrepv = {0}'.format(slrepv))
    print('hlrepv = {0}'.format(hlrepv))

    x = [x for x in range(4096)]
    plt.figure()
    plt.subplot(3, 1, 1)
    plt.title('Original signal')
    plt.plot(x, od1)
    plt.subplot(3, 1, 2)
    plt.title('Signal processed by st')
    plt.plot(x, spd)
    plt.subplot(3, 1, 3)
    plt.title('Signal processed by ht')
    plt.plot(x, hpd)

    plt.tight_layout()
    plt.show()