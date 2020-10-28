import numpy as np
import math as mt


class BlockThMethod:
    def __init__(self, dlist):
        self.data = dlist

    def dividedblock(self):
        dl = len(self.data)
        dbl = int(mt.log(dl))
        dbn = dl // dbl
        DB = []
        for i in range(dbn+1):
            db = []
            if i == dbn:
                if dl - i * dbl == 0:
                    break
                else:
                    for x in range(dl - i * dbl):
                        db.append(self.data[i * dbl + x])
            else:
                for x in range(dbl):
                    db.append(self.data[i * dbl + x])
            DB.append(db)
        return DB

    def blockths(self):
        DB = self.dividedblock()
        TH = []
        n = len(self.data)
        for db in DB:
            sw = 0
            for w in db:
                sw = sw + w ** 2
            er = np.median([abs(x) for x in db]) / 0.6745
            th = 4.50524 * len(db) * er ** 2 / sw
            TH.append(th)
        return TH

    def recoverdata(self, DB):
        d = []
        for db in DB:
            for w in db:
                d.append(w)
        return d


if __name__ == '__main__':
    t1 = BlockThMethod([x for x in range(27)])
    a = t1.dividedblock()
    b = t1.blockths()
    c = t1.recoverdata(a)
    print(a)
    print(b)
    print(c)
