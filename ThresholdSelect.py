import numpy as np
import math as mt


class ThSelect:
    def __init__(self, alist):
        self.ogdata = alist

    def DonohoThEx(self):
        m = np.median([abs(x) for x in self.ogdata]) / 0.6745
        N = len(self.ogdata)
        lgN = mt.log(N)
        th = m * (2 * lgN) ** (1 / 2)
        return th

    def DonohoThEx2(self, level):
        m = np.median([abs(x) for x in self.ogdata]) / 0.6745
        N = len(self.ogdata)/2**(level-1)
        lgN = mt.log(N)
        th = m * (2 * lgN) ** (1 / 2)
        return th

    def EntropyTh1(self):
        sn = int(mt.log(len(self.ogdata)))
        n = len(self.ogdata)//sn
        shes = []
        for i in range(n):
            eg = 0
            for j in range(i*sn, i*sn+sn):
                eg = eg + self.ogdata[j]**2
            she = 0
            for j in range(i*sn, i*sn+sn):
                p = self.ogdata[j]**2 / eg
                she = she - p*mt.log(p)
            shes.append(she)
        if len(self.ogdata) % sn != 0:
            eg = 0
            for j in range(n * sn, len(self.ogdata)):
                eg = eg + self.ogdata[j] ** 2
            she = 0
            for j in range(n * sn, len(self.ogdata)):
                p = self.ogdata[j] ** 2 / eg
                she = she - p * mt.log(p)
            shes.append(she)
        else:
            pass
        maxshe = np.max(shes)
        idmax = shes.index(maxshe)
        if idmax < n:
            m = np.median([abs(x) for x in self.ogdata[idmax*sn: idmax*sn+sn]])
        else:
            m = np.median([abs(x) for x in self.ogdata[idmax * sn: len(self.ogdata)]])
        N = len(self.ogdata)
        lgN = mt.log(N)
        th = m * (2 * lgN) ** (1 / 2)
        return th

    def EntropyTh2(self):
        N = len(self.ogdata)
        eg = 0
        she = 0
        for i in range(N):
            eg = eg + self.ogdata[i]**2
        for i in range(N):
            p = self.ogdata[i]**2 / eg
            if p == 0:
                p = mt.e**(-10)
            she = she - p*mt.log(p)
        m = np.median([abs(x) for x in self.ogdata]) / 0.6745
        lgN = mt.log(N)
        th = she * m * (2 * lgN) ** (1 / 2)
        return th


if __name__ == '__main__':
    t1 = ThSelect([x for x in range(100)]).DonohoThEx()
    t2 = ThSelect([x for x in range(1, 101)]).EntropyTh1()
    print(t1)
    print(t2)
