from statsmodels.stats.diagnostic import acorr_ljungbox
import numpy as np
import math as mt
from WtProcess import DWTP


class LayerSelect:
    def __init__(self, aldata, wtname):
        self.data = aldata
        self.wtname = wtname

    def WNrecgSelect(self):
        coeffs = DWTP(self.data).dwtdec(wtname=self.wtname)
        ln = len(coeffs)
        sl = 0
        stop = False
        for i in range(ln - 1, 0, -1):
            ld = coeffs[i]
            if len(ld) < 6:
                break
            elif len(ld) < 80:
                sn = [x for x in range(1, len(ld)//2, 1)]
            else:
                sn = [x for x in range(1, 40, 1)]
            wnr = acorr_ljungbox(ld, sn, return_df=False)  # ld至少有六个元素
            for p in wnr[1]:
                if p < 0.05:
                    stop = True  # 任一延迟阶数的p值小于0.05，认为该层不是白噪声序列
                else:
                    pass
            if stop:
                break
            else:
                sl += 1
        return sl

    def EntropySelect(self):
        maxl = DWTP(self.data).maxdeclevel(self.wtname)
        R = []
        dR = []
        for j in range(maxl):
            coeffs = DWTP(self.data).dwtdec(self.wtname, delevel=j+1)
            er = np.median([abs(x) for x in coeffs[-(j+1)]]) / 0.6745
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
        if len(R) < 3:
           dl = len(R)
        else:
            for i in range(len(R) - 2):
                dr = (R[i + 2] - R[i + 1]) / (R[i + 1] - R[i])
                dR.append(dr)
            maxdr = np.max(dR)
            dl = dR.index(maxdr)
        return dl

    def EntropySelect2(self):
        maxl = DWTP(self.data).maxdeclevel(self.wtname)
        R = []
        dR = []
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
            maxdr = np.max(R)
            dl = R.index(maxdr)
            s= np.sum(R)
        return dl


if __name__ == '__main__':
    # t1 = LayerSelect([[25.75], [-6.25], [-5.30330086, -4.24264069], [-3., 0.5, -1., 0.],
    #                   [-0.70710678, -0.70710678, -1.41421356, 3.53553391, -1.41421356, -1.41421356, -0.70710678]])
    t1 = LayerSelect([1,2,4,5,6,8,9,4,5,7,6,8,9,10],'db2')
    a = t1.WNrecgSelect()
    b = t1.EntropySelect()
    print(a, b)
