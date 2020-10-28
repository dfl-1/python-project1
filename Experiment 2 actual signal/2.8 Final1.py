from GetActualSignal import GetActualSignal
import math as mt
from ThresholdSelect import ThSelect
from BestThEstimation import BestThEstimate
from ThSearchAlgorithm import ThSearchAlgorithm
from WtProcess import SWTP, DWTP
from DenoiseResult import DenoiseRsult
from NoiseDetection import NoiseDetection

if __name__ == '__main__':
    ad = GetActualSignal()
    ad.getwhvalue()
    od = ad.selectvalue(start=0)
    ln = len(od)//1024
    spd = []
    hpd = []
    npd = []
    dl = 3
    for k in range(ln):
        od1 = od[k*1024: k*1024+1024]
        swt = SWTP(od1)
        dwt = DWTP(od1)
        coeffs = swt.swtdec(wtname='db2', delevel=dl)
        dcoeffs = dwt.dwtdec(wtname='db2', delevel=dl)
        n1coeffs = swt.thprocess(coeffs, thf='soft')
        n2coeffs = swt.thprocess(coeffs, thf='hard')
        spd1 = swt.swtrec(n1coeffs, wtname='db2')
        hpd1 = swt.swtrec(n2coeffs, wtname='db2')

        shes = NoiseDetection(od1, 'db2').Entropymethod1(4)
        gth2s = []
        gth3s = []
        for i in range(1, len(coeffs)):
            gth = ThSelect(coeffs[i]).DonohoThEx()
            gth3 = ThSelect(dcoeffs[i]).EntropyTh2()
            if shes[i - 1] > 1.5:
                shes[i - 1] = 1.5
            elif shes[i - 1] < 0.8:
                shes[i - 1] = 0.8
            else:
                pass
            gth2 = gth * shes[i - 1]
            gth2s.append(gth2)
            gth3s.append(gth3)
        ncoeffs3 = swt.thprocess2(coeffs, ths=gth2s, thf='thf3', thps=[2 + 2 * k for k in range(dl)])
        npd1 = swt.swtrec(ncoeffs3, wtname='db2')
        for j in range(len(spd1)):
            spd.append(spd1[j])
            hpd.append(hpd1[j])
            npd.append(npd1[j])
    ad.outputdata(startidex=0, ogdata=od[0:len(spd)-1], pddata=npd)
