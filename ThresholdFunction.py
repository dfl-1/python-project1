import numpy as np
import math as mt
import matplotlib.pyplot as plt
from sympy import *


class ThFuction:
    def __init__(self, alist):
        self.ogdata = alist

    def thsoft(self, th):
        rdata = []
        for x in self.ogdata:
            if abs(x) > th:
                rx = np.sign(x) * (abs(x) - th)
            else:
                rx = 0
            rdata.append(rx)
        return rdata

    def thhard(self, th):
        rdata = []
        for x in self.ogdata:
            if abs(x) > th:
                rx = x
            else:
                rx = 0
            rdata.append(rx)
        return rdata

    def thsemisf(self, th1, th2=None):
        if not th2:
            th2 = 2*th1
        rdata = []
        if th1 > th2:
            raise ValueError('th1 must less than th2')
        for x in self.ogdata:
            if abs(x) > th2:
                rx = x
            else:
                if abs(x) > th1:
                    rx = np.sign(x) * (th2 * (abs(x) - th1) / (th2 - th1))
                else:
                    rx = 0
            rdata.append(rx)
        return rdata

    def thsemisffuzzy(self, clist, th):
        n = len(self.ogdata)
        D = 0
        for i in range(n):
            D = D + (self.__fuzzyfuction(clist, clist[i]) - self.__fuzzyfuction(self.ogdata, self.ogdata[i])) ** 2
        C = (D / n) ** (1 / 2)
        th1 = C * th
        rdata = self.thsemisf(th1, th)
        return rdata

    def __fuzzyfuction(self, elist, x):
        a = 1
        b = -4
        c = abs(elist[0])
        for u in elist:
            if abs(u) < c:
                c = abs(u)
            else:
                pass
        if abs(x) < c:
            fu = 0
        else:
            fu = 1 / (1 + (a * (abs(x) - c)) ** b)
        return fu

    def thf1(self, th, m):
        rdata = []
        for x in self.ogdata:
            if abs(x) > th:
                rx = x - np.sign(x) * m * (th / mt.e ** ((abs(x) ** 2 - th ** 2) ** (1 / 2)))
            else:
                rx = 0
            rdata.append(rx)
        return rdata

    def thf2(self, th, a):
        rdata = []
        for x in self.ogdata:
            if abs(x) > th:
                rx = x - 0.5 * np.sign(x) * (th ** a / abs(x) ** (a - 1))
            else:
                rx = 0.5 * np.sign(x) * (abs(x) ** (a + 1) / th ** a)
            rdata.append(rx)
        return rdata

    def thf2dx(self, th, a):
        rd = []
        for x in self.ogdata:
            if abs(x) > th:
                rx = 1 - 0.5 * (1 - a) * (th ** a / abs(x) ** a)
            else:
                rx = 0.5 * (a + 1) * (abs(x) ** a / th ** a)
            rd.append(rx)
        return rd

    def thf3(self, th, a):
        rdata = []
        for x in self.ogdata:
            if x == 0:
                rx = 0
            else:
                rx = x * 2 ** (-abs(th / x) ** a)
            rdata.append(rx)
        return rdata

    def thf3dx(self, th, a):
        rd = []
        for x in self.ogdata:
            if x == 0:
                rx = 0
            else:
                rx = 2 ** (-abs(th / x) ** a) * a * (th / x) ** a * mt.log(2) + 2 ** (-abs(th / x) ** a)
            rd.append(rx)
        return rd


if __name__ == '__main__':
    x = symbols('x')
    th = symbols('th')
    a = symbols('a')
    rx = diff(x * 2 ** (-(th / x) ** a), x)
    print(rx)

    od = [x / 20 for x in range(-100, 100)]
    tic = [x for x in range(-10, 12, 2)]

    t1 = ThFuction(od)
    plt.figure()
    plt.xticks(tic)
    plt.yticks(tic)
    l1, = plt.plot(od, t1.thhard(1), linestyle='-')
    l2, = plt.plot(od, t1.thsoft(1), linestyle='-.')
    l3, = plt.plot(od, t1.thsemisf(1, 2), linestyle='dashed')
    l4, = plt.plot(od, t1.thf1(1, 0.8), linestyle='--')
    l5, = plt.plot(od, t1.thf2(1, 2), linestyle='solid')
    l6, = plt.plot(od, t1.thf3(1, 4), linestyle='dashdot')
    plt.legend(handles=[l1, l2, l3, l4, l5, l6], labels=['hard', 'soft', 'semisoft', 'th1m0.5', 'th2a2', 'th3a4'])
    plt.show()

    plt.figure()
    plt.xticks(tic)
    plt.yticks(tic)
    l7, = plt.plot(od, t1.thf2dx(1, 4), linestyle='solid')
    l8, = plt.plot(od, t1.thf3dx(1, 4), linestyle='dashdot')
    plt.legend(handles=[l7, l8], labels=['th2dxa4', 'th3dxa4'])
    plt.show()

    t2 = ThFuction(od)
    plt.figure()
    plt.xticks(tic)
    plt.yticks(tic)
    l1, = plt.plot(od, t1.thhard(1), linestyle='-')
    l2, = plt.plot(od, t1.thsoft(1), linestyle='-.')
    l3, = plt.plot(od, t1.thf3(1, 2), linestyle='dashed')
    l4, = plt.plot(od, t1.thf3(1, 4), linestyle='--')
    l5, = plt.plot(od, t1.thf3(1, 6), linestyle='solid')
    l6, = plt.plot(od, t1.thf3(1, 10), linestyle='dashdot')
    plt.legend(handles=[l1, l2, l3, l4, l5, l6], labels=['hard', 'soft', 'th3a2', 'th3a4', 'th3a6', 'th3a10'])
    plt.show()
