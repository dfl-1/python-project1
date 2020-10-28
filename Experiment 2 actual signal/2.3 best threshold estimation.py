from GetActualSignal import GetActualSignal
import math as mt
from BlockThMethod import BlockThMethod
from ThresholdSelect import ThSelect
from BestThEstimation import BestThEstimate
from ThSearchAlgorithm import ThSearchAlgorithm
from WtProcess import DWTP
from DenoiseResult import DenoiseRsult
from AcSNR import AcSNR

if __name__ == '__main__':
    ad = GetActualSignal()
    ad.getwhvalue()
    od1 = ad.selectvalue(start=6000, end=7024)
    dl = 4
    dwd = DWTP(od1)
    coeffs = dwd.dwtdec(wtname='db2', delevel=dl)
    gths = []
    bsths = []
    for i in range(1, len(coeffs)):
        bthe = BestThEstimate(coeffs[i], thfunction='thf3', thp=2 + 2 * i)
        thsa = ThSearchAlgorithm()
        gth = ThSelect(coeffs[i]).DonohoThEx()
        bsth = thsa.FibonacciSearch(bthe.msesurefuction, [0, 1.5 * gth], 0.01)
        gths.append(gth)
        bsths.append(bsth)

    ncoeffs1 = dwd.thprocess2(coeffs, ths=gths, thf='thf3', thps=[2 + 2 * k for k in range(dl)])
    ncoeffs2 = dwd.thprocess2(coeffs, ths=bsths, thf='thf3', thps=[2 + 2 * k for k in range(dl)])
    gthpd = dwd.dwtrec(ncoeffs1, wtname='db2')
    bsthpd = dwd.dwtrec(ncoeffs2, wtname='db2')
    ad.outputdata(startidex=5000, ogdata=od1, pddata=bsthpd)
    bsm = DenoiseRsult([], bsthpd).smooth(od1)
    blrepv = DenoiseRsult([], bsthpd).lrepv(od1, 128)
    print('bsm = {0}'.format(bsm))
    print('blrepv = {0}'.format(blrepv))