import codecs
import csv


class GetActualSignal:
    def __init__(self):
        self.ogdata = []

    def getwhvalue(self):
        data = []
        with open(r'C:\Users\Jason\Desktop\input.csv', 'r') as f:
            reader = csv.reader(f)
            for i in reader:
                data.append(float(i[1]))
        self.ogdata = data

    def selectvalue(self, start=0, end=None):
        if not end:
            end = len(self.ogdata)-1
        sdata = self.ogdata[start:end]
        return sdata

    def outputdata(self,startidex, ogdata, pddata):
        index = [startidex+i for i in range(len(ogdata))]
        strdata = []
        for i in range(len(index)):
            strdata.append(str(index[i]) + ',' + str(ogdata[i]) + ',' + str(pddata[i]))
        f2 = codecs.open(r'C:\Users\Jason\Desktop\output.csv', 'w', 'utf-8')
        for n in strdata:
            writer = csv.writer(f2, delimiter='\t', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(n)
        f2.close()


if __name__ == '__main__':
    t1 = GetActualSignal()
    t1.getwhvalue()
    sd = t1.selectvalue(19700, 20700)
    t1.outputdata(19700, sd, sd)
