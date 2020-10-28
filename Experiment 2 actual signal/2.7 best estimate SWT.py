from GetActualSignal import GetActualSignal
import math as mt
from BlockThMethod import BlockThMethod
from ThresholdSelect import ThSelect
from BestThEstimation import BestThEstimate
from ThSearchAlgorithm import ThSearchAlgorithm
from WtProcess import SWTP
from DenoiseResult import DenoiseRsult
from NoiseDetection import NoiseDetection

if __name__ == '__main__':
    ad = GetActualSignal()
    ad.getwhvalue()
    od1 = ad.selectvalue(start=11000, end=12024)
    dl = 3
    swd = SWTP(od1)
    coeffs = swd.swtdec(wtname='db2', delevel=dl)
    gths = []
    gth2s = []
    bsths = []
    shes = NoiseDetection(od1, 'db2').Entropymethod1(4)
    for i in range(1, len(coeffs)):
        bthe = BestThEstimate(coeffs[i], thfunction='thf3', thp=2 + 2 * i)
        thsa = ThSearchAlgorithm()
        gth = ThSelect(coeffs[i]).DonohoThEx()
        if shes[i-1] > 1.5:
            shes[i-1] = 1.5
        elif shes[i-1] < 0.8:
            shes[i-1] = 0.8
        else:
            pass
        gth2 = gth*shes[i-1]
        bsth = thsa.FibonacciSearch(bthe.msesurefuction, [0, 1.5 * gth], 0.01)
        gths.append(gth)
        gth2s.append(gth2)
        bsths.append(bsth)

    # tths = [0.6*gths[0], 0.8*gths[1], 1.2*gths[2], 1.4*gths[3]]
    # tths2 = [bsths[0], bsths[1], 2*bsths[2], 3*bsths[3]]
    ncoeffs1 = swd.thprocess2(coeffs, ths=gths, thf='thf3', thps=[2 + 2 * k for k in range(dl)])
    ncoeffs2 = swd.thprocess2(coeffs, ths=bsths, thf='thf3', thps=[2 + 2 * k for k in range(dl)])
    ncoeffs3 = swd.thprocess2(coeffs, ths=gth2s, thf='thf3', thps=[2 + 2 * k for k in range(dl)])
    gthpd = swd.swtrec(ncoeffs1, wtname='db2')
    bsthpd = swd.swtrec(ncoeffs2, wtname='db2')
    tthpd = swd.swtrec(ncoeffs3, wtname='db2')
    ad.outputdata(startidex=11000, ogdata=od1, pddata=tthpd)
    bsm = DenoiseRsult([], bsthpd).smooth(od1)
    blrepv = DenoiseRsult([], bsthpd).lrepv(od1, 128)
    print('bsm = {0}'.format(bsm))
    print('blrepv = {0}'.format(blrepv))