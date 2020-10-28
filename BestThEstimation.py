from ThresholdFunction import ThFuction
import numpy as np
import sys


class BestThEstimate:
    def __init__(self, alist, thfunction='', thp=None):
        self.data = alist
        self.thfucname = thfunction
        self.thp = thp

    def cvalfunction(self, th):
        thf = ThFuction(self.data)
        if self.thfucname == 'soft':
            tdata = thf.thsoft(th)
        elif self.thfucname == 'hard':
            tdata = thf.thhard(th)
        elif self.thfucname == 'thf1':
            tdata = thf.thf1(th, self.thp)
        elif self.thfucname == 'thf2':
            tdata = thf.thf2(th, self.thp)
        elif self.thfucname == 'thf3':
            tdata = thf.thf3(th, self.thp)
        else:
            raise ValueError('thfunction must be "soft","hard","thf1","thf2","thf3"')
        fe = []
        fo = []
        tfe = []
        tfo = []

        for i in range(len(self.data) // 2):
            e = self.data[2 * i]
            o = self.data[2 * i + 1]
            te = tdata[2 * i]
            to = tdata[2 * i + 1]
            fe.append(e)
            fo.append(o)
            tfe.append(te)
            tfo.append(to)
        efe = []
        efo = []
        for i in range(len(fe) - 1):
            efo.append((fe[i] + fe[i + 1]) / 2)
            efe.append((fo[i] + fo[i + 1]) / 2)
        isee = 0
        iseo = 0
        for i in range(len(efo)):
            isee = isee + (tfe[i] - efe[i]) ** 2
            iseo = iseo + (tfo[i] - efo[i]) ** 2
        ISE = isee + iseo
        return ISE

    def gcvfunction(self, th):
        thf = ThFuction(self.data)
        n = len(self.data)
        if self.thfucname == 'soft':
            tdata = thf.thsoft(th)
            n0 = 0
            for w in self.data:
                if abs(w) < th:
                    n0 += 1
                else:
                    pass
        else:
            if self.thfucname == 'thf2':
                tdata = thf.thf2(th, self.thp)
                dxtd = thf.thf2dx(th, self.thp)
                n0 = 0
                for dw in dxtd:
                    n0 = n0 + (1 - dw)
            elif self.thfucname == 'thf3':
                tdata = thf.thf3(th, self.thp)
                dxtd = thf.thf3dx(th, self.thp)
                n0 = 0
                for dw in dxtd:
                    n0 = n0 + (1 - dw)
            else:
                raise ValueError('thfunction must be "soft","thf2","thf3"')
        ff2 = 0
        for i in range(n):
            ff2 = ff2 + (self.data[i] - tdata[i]) ** 2
        if n0 == 0:
            gcv = sys.maxsize
        else:
            gcv = ff2 * n / n0 ** 2
        return gcv

    def msesurefuction(self, th):
        v = np.median([abs(x) for x in self.data]) / 0.6745
        thf = ThFuction(self.data)
        if self.thfucname == 'thf2':
            tdata = thf.thf2(th, self.thp)
            tdatadx = thf.thf2dx(th, self.thp)
        elif self.thfucname == 'thf3':
            tdata = thf.thf3(th, self.thp)
            tdatadx = thf.thf3dx(th, self.thp)
        else:
            raise ValueError('thfunction must be "thf2","thf3"')
        gy2 = 0
        for i in range(len(self.data)):
            gy2 = gy2 + (tdata[i] - self.data[i]) ** 2
        dgy = 0
        for i in range(len(self.data)):
            dgy = dgy + tdatadx[i] - 1
        Rs = gy2 + 2 * v ** 2 * dgy
        return Rs


if __name__ == '__main__':
    t1 = BestThEstimate([x for x in range(-10, 20)], 'thf3', 4)
    a = t1.cvalfunction(2)
    b = t1.gcvfunction(2)
    c = t1.msesurefuction(2)
    print(a)
    print(b)
    print(c)
