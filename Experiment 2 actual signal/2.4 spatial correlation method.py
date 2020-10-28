from GetActualSignal import GetActualSignal
import math as mt
from BlockThMethod import BlockThMethod
from ThresholdSelect import ThSelect
from BestThEstimation import BestThEstimate
from ThSearchAlgorithm import ThSearchAlgorithm
from WtProcess import SWTP
from DenoiseResult import DenoiseRsult
from SpatialCorrelationThresholdALG import SpCoThALG

if __name__ == '__main__':
    ad = GetActualSignal()
    ad.getwhvalue()
    od1 = ad.selectvalue(start=10000, end=14096)
    dl = 4
    swt = SWTP(od1)
    coeffs = swt.swtdec(wtname='sym6', delevel=dl)
    spta = SpCoThALG(coeffs)
    nce1s = spta.spcoThf1()
    sf1pd = swt.swtrec(nce1s, wtname='sym6')

    spta2 = SpCoThALG(coeffs)
    sfp1ths = []
    sfp2ths = []
    gpths = []
    P = spta2.spcoCors()
    for i in range(1, len(coeffs) - 1):
        spta2.BTHassitIndex(i, pk=0.1, pa=4, mode='srmse')
        gpth = ThSelect(P[i - 1]).DonohoThEx()
        sfp1th = ThSearchAlgorithm().FibonacciSearch(spta2.BTHspcothfwp1, [0, 1.5 * gpth], 0.01)
        sfp2th = ThSearchAlgorithm().FibonacciSearch(spta2.BTHspcothfwp2, [0, 1.5 * gpth], 0.01)
        gpths.append(gpth)
        sfp1ths.append(sfp1th)
        sfp2ths.append(sfp2th)
    npce1s = spta2.spcoThfwp1(sfp1ths, 0.05)
    npce2s = spta2.spcoThfwp2(sfp2ths, 4)
    sfp1pd = swt.swtrec(npce1s, wtname='sym6')
    sfp2pd = swt.swtrec(npce2s, wtname='sym6')
    ad.outputdata(startidex=10000, ogdata=od1, pddata=sfp2pd)

    sf1sm = DenoiseRsult([], sf1pd).smooth(od1)
    sfp1sm = DenoiseRsult([], sfp1pd).smooth(od1)
    sfp2sm = DenoiseRsult([], sfp2pd).smooth(od1)

    sf1lrepv = DenoiseRsult([], sf1pd).lrepv(od1, 128)
    sfp1lrepv = DenoiseRsult([], sfp1pd).lrepv(od1, 128)
    sfp2lrepv = DenoiseRsult([], sfp2pd).lrepv(od1, 128)

    print('sf1sm = {0}'.format(sf1sm))
    print('sfp1sm = {0}'.format(sfp1sm))
    print('sfp2sm = {0}'.format(sfp2sm))
    print('sf1lrepv = {0}'.format(sf1lrepv))
    print('sfp1lrepv = {0}'.format(sfp1lrepv))
    print('sfp2lrepv = {0}'.format(sfp2lrepv))