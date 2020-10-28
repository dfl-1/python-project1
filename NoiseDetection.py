from statsmodels.stats.diagnostic import acorr_ljungbox
import numpy as np
import math as mt
from WtProcess import DWTP


class NoiseDetection:
    def __init__(self, aldata, wtname):
        self.data = aldata
        self.wtname = wtname

    def WNrecgmethod(self):
        coeffs = DWTP(self.data).dwtdec(wtname=self.wtname)
        ln = len(coeffs)
        mps =[]
        for i in range(1, ln):
            ld = coeffs[i]
            if len(ld) < 6:
                break
            elif len(ld) < 200:
                sn = [x for x in range(1, len(ld) // 2, 1)]
            else:
                sn = [x for x in range(1, 200, 1)]
            wnr = acorr_ljungbox(ld, sn, return_df=False)  # ld至少有六个元素
            mp = np.average(wnr[1])
            mps.append(mp)
        return mps

    def Entropymethod1(self, delevel):
        coeffs = DWTP(self.data).dwtdec(wtname=self.wtname, delevel=delevel)
        ln = len(coeffs)
        shes = []
        for i in range(1, ln):
            ces = coeffs[i]
            eg = 0
            for j in range(len(ces)):
                eg = eg + ces[j]**2
            she = 0
            for j in range(len(ces)):
                p = ces[j]**2/eg
                if p == 0:
                    p = mt.e**(-10)
                she = she - p*mt.log(p)
            shes.append(she)
        return shes

    def Entropymethod2(self):
        maxl = DWTP(self.data).maxdeclevel(self.wtname)
        R = []
        SN=[]
        for j in range(maxl):
            coeffs = DWTP(self.data).dwtdec(self.wtname, delevel=j + 1)
            er = np.median([abs(x) for x in coeffs[-(j + 1)]]) / 0.6745
            sher = 0.5 * mt.log(2 * mt.pi * mt.e * er ** 2)
            ln = len(coeffs)
            EG = 0
            egl = []
            for i in range(ln):
                lce = coeffs[i]
                eg = 0
                for ce in lce:
                    eg = eg + ce ** 2
                egl.append(eg)
                EG = EG + eg

            P = []
            p = egl[0] / EG
            P.append(p)
            shfs = []
            for i in range(1, ln):
                p = egl[i] / EG
                P.append(p)
                shf = 0
                for p in P:
                    shf = shf - p * mt.log(p)
                shfs.append(shf)
            r = shf / sher
            R.append(r)
            SN.append(sher)
        return SN


