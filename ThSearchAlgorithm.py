import math as mt
from sympy import *


class ThSearchAlgorithm:
    def GoldcutSearch(self, func, rg, e):
        a = rg[0]
        b = rg[1]
        while b - a > e:
            d = b - a
            l = a + 0.382 * d
            h = a + 0.618 * d
            if func(l) > func(h):
                a = l
            else:
                b = h
        return (a + b) / 2

    def __FibonacciGN(self, n):
        if n == 0 or n == 1:
            return 1
        else:
            return self.__FibonacciGN(n - 1) + self.__FibonacciGN(n - 2)

    def FibonacciSearch(self, fun, rg, e):
        a = rg[0]
        b = rg[1]
        n = 0
        while self.__FibonacciGN(n) < (b - a) / e:
            n = n + 1
        while n > 1:
            d = b - a
            l = a + self.__FibonacciGN(n - 2) / self.__FibonacciGN(n) * d
            h = a + self.__FibonacciGN(n - 1) / self.__FibonacciGN(n) * d
            if fun(l) > fun(h):
                a = l
            else:
                b = h
            n -= 1
        return l

    def NewtonApproxi(self, func, start, e):
        x = start
        while (self.diffFunc(func, x, 1)) > e:
            x = x - self.diffFunc(func, x, 1) / self.diffFunc(func, x, 2)
        return x

    def RationalInterpolation(self, func, x, h, e, n):
        xdata = []
        zdata = []
        a = x
        for i in range(n):
            x = a + i * h
            xdata.append(x)
        for x in xdata:
            z = self.diffFunc(func, x)
            zdata.append(z)
        zn = 10
        while abs(zn) > e:
            d = [x for x in xdata]  # d0层参数
            a = 1
            while a < n:
                for i in range(a, len(d)):
                    d[i] = (zdata[i] - zdata[a - 1]) / (d[i] - d[a - 1])
                a += 1
            b = d
            r = b[len(b) - 1]
            for i in range(len(d) - 2, -1, -1):
                r = b[i] - zdata[i] / r
            xn = r
            xdata.append(xn)
            zn = self.diffFunc(func, xn)
            zdata.append(zn)
            n += 1
        return xn

    def FastdownSearch(self, func, start, e):
        x = start
        d = 10
        while abs(d) > e:
            d = -self.diffFunc(func, x)
            if d == 0:
                break
            h = symbols('h')
            eq = self.diffFunc(func, x + h * d)
            a = solve(eq, h)
            s = a[0]
            x = x + s * d
        return x

    def diffFunc(self, func, value, s=1):
        x = symbols('x')
        r = diff(func(x), x, s).subs(x, value)
        return r


if __name__ == '__main__':
    def func1(x):
        return 2 * x ** 2 - x - 1


    def func2(x):
        r = (mt.e ** x) / 2
        return r


    t1 = ThSearchAlgorithm()
    print(t1.GoldcutSearch(func1, [-1, 1], 0.16))
    print(t1.FibonacciSearch(func1, [-1, 1], 0.16))
    print(t1.NewtonApproxi(func2, 0.5, 0.001))
    print(t1.RationalInterpolation(func2, 0.5, 0.5, 0.0001, 4))
    # h=symbols('h')
    # a=solve(0.5*2.718288888**(0.5-round(0.866666,1)*h)-0.1,h)
    # print(a)
    print(t1.FastdownSearch(func1, 0.5, 0.1))
