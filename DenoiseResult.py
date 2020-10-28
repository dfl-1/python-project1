import math as mt


class DenoiseRsult:
    def __init__(self, tdata, pdata):
        self.tdata = tdata
        self.pdata = pdata

    def snr(self):
        a = 0
        for i in range(len(self.tdata)):
            a = a + self.pdata[i] ** 2 / (self.tdata[i] - self.pdata[i]) ** 2
        snr = 10 * mt.log10(a)
        return snr

    def mse(self):
        a = 0
        for i in range(len(self.tdata)):
            a = a + (self.tdata[i] - self.pdata[i]) ** 2
        mse = a / len(self.pdata)
        return mse

    def smooth(self,origdata):
        osm = 0
        psm = 0
        n = len(self.pdata)
        for i in range(n-1):
            osm = osm + (origdata[i+1]-origdata[i])**2
            psm = psm + (self.pdata[i+1]-self.pdata[i])**2
        sm =(psm/osm)**2
        return sm

    def lrepv(self, origdata, lcn):
        olcps = []
        plcps = []
        sn = len(self.pdata)
        m = int(sn / lcn)
        for i in range(m):
            op = origdata[i * lcn]
            pp = self.pdata[i * lcn]
            for j in range(i * lcn, (i + 1) * lcn):
                if origdata[j] > op:
                    op = origdata[j]
                else:
                    pass
                if self.pdata[j] > pp:
                    pp = self.pdata[j]
                else:
                    pass
            olcps.append(op)
            plcps.append(pp)
        for j in range((m - 1) * lcn, sn):
            if origdata[j] > op:
                op = origdata[j]
            else:
                pass
            if self.pdata[j] > pp:
                pp = self.pdata[j]
            else:
                pass
        olcps.append(op)
        plcps.append(pp)
        r = 0
        for i in range(len(olcps)):
            r = r + abs(olcps[i] - plcps[i]) / abs(olcps[i])
        lrepv = r / lcn
        return lrepv


if __name__ == '__main__':
    d1 = [x for x in range(20)]
    d2 = [x + 0.2 for x in range(20)]
    d3 = [x + 0.1 for x in range(20)]
    t1 = DenoiseRsult(d1, d3)
    a = t1.snr()
    b = t1.mse()
    c = t1.lrepv(d2, 7)
    d = t1.smooth(d2)
    print(a, b, c, d)
