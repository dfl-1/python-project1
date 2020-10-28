import math as mt
from sympy import symbols
from sympy import diff


class smt:
    def diffFunc(self, fun, value, s=1):
        x = symbols('x')
        return diff(fun(x), x, s).subs(x, value)

    def gtan(self, pa, data):
        max = data[0]
        min = max
        for i in data:
            if i > max:
                max = i
            if i < min:
                min = i
        d = max - min
        rlist = []
        pi = mt.pi
        for i in data:
            rlist.append(mt.tan(i * pi * pa / (2 * d)))
        return rlist

    def grtan(self, pa, data):
        max = data[0]
        min = max
        for i in data:
            if i > max:
                max = i
            if i < min:
                min = i
        d = max - min
        rlist = []
        pi = mt.pi
        for i in data:
            rlist.append(mt.atan(i * 2 * d / (pa * pi)))
        return rlist

    def __FibonacciGN(self, n):
        if n == 0 or n == 1:
            return 1
        else:
            return self.__FibonacciGN(n - 1) + self.__FibonacciGN(n - 2)

    def FibonacciSearch(self, data, key):
        dl = len(data)
        n = 0
        while dl > self.__FibonacciGN(n):
            n += 1
        dl2 = self.__FibonacciGN(n)
        data2 = []
        for i in range(dl):
            data2.append(data[i])
        for i in range(dl, dl2):
            data2.append(data[dl - 1])
        low = 0
        high = dl2 - 1
        while high > low:
            min = low + self.__FibonacciGN(n - 1) - 1
            if key < data2[min]:
                high = min
                n -= 1
            elif key > data2[min]:
                low = min + 1
                n -= 2
            else:
                if min < dl:
                    return min
                else:
                    return dl - 1
        return -1
