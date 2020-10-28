from ThresholdSelect import ThSelect
import numpy as np
import math as mt


class SpCoThALG:
    def __init__(self, coeffs):
        self.coeffs = coeffs  # coeffs应分解到最佳层数的上一层
        self.level = 1
        self.mode = None
        self.pk = 0
        self.pa = 0

    def spcoCors(self):
        cors = []
        p = []
        for i in range(len(self.coeffs) - 1, 1, -1):
            for k in range(len(self.coeffs[i])):
                sc = self.coeffs[i][k] * self.coeffs[i - 1][k]
                p.append(sc)
            cors.append(p)  # 分解层次由高到低
        return cors

    def nlEcors(self):
        cors = self.spcoCors()
        pws = []
        pcors = []
        pw = 0
        for i in range(len(self.coeffs) - 1, 1, -1):
            for k in range(len(self.coeffs[i])):
                pw = pw + self.coeffs[i][k] ** 2
            pws.append(pw)
        pcor = 0
        for cor in cors:
            for p in cor:
                pcor = pcor + p ** 2
            pcors.append(pcor)
        Ecors = []
        Ecor = []
        for i in range(len(cors)):
            for p in cors[i]:
                ec = p * (pws[i] / pcors[i]) ** 0.5
                Ecor.append(ec)
            Ecors.append(Ecor)
        return Ecors  # Ecors的层数比coeffs少两层

    def spcoThf1(self):
        Ecors = self.nlEcors()
        ncoeffs = []
        for i in range(1, len(self.coeffs) - 1):
            W = self.coeffs[-i]
            nW = []
            ec = Ecors[i - 1]
            for k in range(len(W)):
                if abs(ec[k]) < abs(W[k]):
                    w = 0
                else:
                    w = W[k]
                nW.append(w)
            ncoeffs.insert(0, np.asarray(nW))
        ncoeffs.insert(0, self.coeffs[1])
        ncoeffs.insert(0, self.coeffs[0])
        return ncoeffs

    def spcoThf2(self):
        Ecors = self.nlEcors()
        ncoeffs = []
        for i in range(1, len(self.coeffs) - 1):
            W = self.coeffs[-i]
            nW = []
            ec = Ecors[i - 1]
            th = ThSelect(W).DonohoThEx()
            for k in range(len(W)):
                thn = abs(W[k]) / abs(ec[k]) * th
                if abs(W[k]) < thn:
                    w = 0
                else:
                    w = W[k]
                nW.append(w)
            ncoeffs.insert(0, np.asarray(nW))
        ncoeffs.insert(0, self.coeffs[1])
        ncoeffs.insert(0, self.coeffs[0])
        return ncoeffs

    def spcoThfwp1(self, pths, pk):
        cors = self.spcoCors()
        ncoeffs = []
        for i in range(1, len(self.coeffs) - 1):
            W = self.coeffs[-i]
            nW = []
            p = cors[i - 1]
            pth = pths[i - 1]
            for k in range(len(W)):
                uf = 1 / (1 + mt.e ** ((pth - p[k]) / pk)) - 1 / (1 + mt.e ** ((-pth - p[k]) / pk)) + 1
                w = uf * W[k]
                nW.append(w)
            ncoeffs.insert(0, np.asarray(nW))
        ncoeffs.insert(0, self.coeffs[1])
        ncoeffs.insert(0, self.coeffs[0])
        return ncoeffs

    def BTHassitIndex(self, i, pk=0, pa=4, mode='srmse'):
        self.level = i
        self.pk = pk
        self.pa = pa
        self.mode = mode

    def BTHspcothfwp1(self, pth):
        # self.level层最佳p阈值
        i = self.level
        pk = self.pk
        cors = self.spcoCors()
        W = self.coeffs[-i]
        p = cors[i-1]
        v = np.median([abs(x) for x in W]) / 0.6745
        gy2 = 0
        for k in range(len(W)):
            gy = (1 / (1 + mt.e ** ((pth - p[k]) / pk)) - 1 / (1 + mt.e ** ((-pth - p[k]) / pk)))*W[k]
            gy2 = gy2 + gy**2
        sdgy = 0
        for k in range(len(W)):
            dgy = 1 / (1 + mt.e ** ((pth - p[k]) / pk)) - 1 / (1 + mt.e ** ((-pth - p[k]) / pk)) + \
                  (p[k] / pk) * (mt.e ** ((pth - p[k]) / pk) / (1 + mt.e ** ((pth - p[k]) / pk))**2 -
                               mt.e ** ((-pth - p[k]) / pk) / (1 + mt.e ** ((-pth - p[k]) / pk))**2)
            if dgy < 0 or dgy > 0:
                sdgy = sdgy + dgy
            else:
                pass
        if self.mode == 'srmse':
            Rs = gy2 + 2 * v ** 2 * sdgy
            return Rs
        elif self.mode == 'gcv':
            gcv = gy2 * len(W) / sdgy ** 2
            return gcv
        else:
            raise ValueError('mode must be "srmse" or "gcv"')

    def spcoThfwp2(self, pths, pa):
        cors = self.spcoCors()
        ncoeffs = []
        for i in range(1, len(self.coeffs) - 1):
            W = self.coeffs[-i]
            nW = []
            p = cors[i - 1]
            pth = pths[i - 1]
            for k in range(len(W)):
                if p[k] == 0:
                    uf = 0
                else:
                    uf = 2 ** (-1 * (pth / p[k]) ** pa)
                w = uf * W[k]
                nW.append(w)
            ncoeffs.insert(0, np.asarray(nW))
        ncoeffs.insert(0, self.coeffs[1])
        ncoeffs.insert(0, self.coeffs[0])
        return ncoeffs

    def BTHspcothfwp2(self, pth):
        # self.level层最佳p阈值
        i = self.level
        pa = self.pa
        cors = self.spcoCors()
        W = self.coeffs[-i]
        p = cors[i - 1]
        v = np.median([abs(x) for x in W]) / 0.6745
        gy2 = 0
        for k in range(len(W)):
            if p[k] == 0:
                gy = 0 - 1 * W[k]
            else:
                gy = (2 ** (-(pth / p[k]) ** pa) - 1) * W[k]
            gy2 = gy2 + gy**2
        dgy = 0
        for k in range(len(W)):
            dgy = dgy + 2 ** (-(pth / p[k]) ** pa) * pa * (pth / p[k]) ** pa * mt.log(2) + 2 ** (-(pth / p[k]) ** pa) - 1
        if self.mode == 'srmse':
            Rs = gy2 + 2 * v ** 2 * dgy
            return Rs
        elif self.mode == 'gcv':
            gcv = gy2 * len(W) / dgy**2
            return gcv
        else:
            raise ValueError('mode must be "srmse" or "gcv"')


if __name__ == '__main__':
    t1 = SpCoThALG(
        [[8.13068967, 5.71562616, 5.43213251, 8.03020872, 11.36931033, 13.78437384, 14.06786749, 11.46979128],
         [-2.17732304, -1.51225953, -0.52123412, 3.82684209, 6.45841195, 1.92732304, -3.75985479, -4.2419056],
         [-1.000601, 0.35355339, 0.12940952, -0.48296291, 0.35355339, 3.027187, -0.18946869, -2.1906707]])
    p = t1.spcoCors()
    ecors = t1.nlEcors()
    ncoeffs = t1.spcoThf1()
    nc2 = t1.spcoThf2()
    nc3 = t1.spcoThfwp1([2], 0.01)
    nc4 = t1.spcoThfwp2([2], 10)
    t1.BTHassitIndex(1, 0.05, 4)
    rs1 = t1.BTHspcothfwp1(1)
    rs2 = t1.BTHspcothfwp2(1)
    print(p)
    print(ecors)
    print(ncoeffs)
    print(nc2)
    print(nc3)
    print(nc4)
    print(rs1, rs2)
