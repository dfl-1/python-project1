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
    od1 = ad.selectvalue(start=11000, end=12024)
    dl = 4
    swt = SWTP(od1)
    coeffs = swt.swtdec(wtname='db2', delevel=dl)
    n1coeffs = swt.thprocess(coeffs, thf='soft')
    n2coeffs = swt.thprocess(coeffs, thf='hard')
    n3coeffs = swt.thprocess(coeffs, thf='thsemisf')
    spd = swt.swtrec(n1coeffs, wtname='db2')
    hpd = swt.swtrec(n2coeffs, wtname='db2')
    thf1pd = swt.swtrec(n3coeffs, wtname='db2')

    ad.outputdata(startidex=0, ogdata=od1, pddata=hpd)

    ssm = DenoiseRsult([], spd).smooth(od1)
    hsm = DenoiseRsult([], hpd).smooth(od1)
    thf1sm = DenoiseRsult([], thf1pd).smooth(od1)

    slrepv = DenoiseRsult([], spd).lrepv(od1, 128)
    hlrepv = DenoiseRsult([], hpd).lrepv(od1, 128)
    thf1lrepv = DenoiseRsult([], thf1pd).lrepv(od1, 128)

    print('sf1sm = {0}'.format(ssm))
    print('sfp1sm = {0}'.format(hsm))
    print('sfp2sm = {0}'.format(thf1sm))
    print('slrepv = {0}'.format(slrepv))
    print('hlrepv = {0}'.format(hlrepv))
    print('sfp2lrepv = {0}'.format(thf1lrepv))