import pywt
import SignalModel
import matplotlib.pyplot as plt


class SWPT:
    def __init__(self, data, wavelet='db3'):
        self.data = data
        self.wavelet = wavelet

    def getPacketCoefficent(self, indexlist):
        if len(indexlist) != 2:
            raise ValueError("indexlist must be [x, y], y<2**x+1, x < maxlevel+1")
        if indexlist[0] == 1:
            if indexlist[1] == 1:
                pc = pywt.swt(data=self.data, wavelet=self.wavelet, level=1, trim_approx=True)[0]
            elif indexlist[1] == 2:
                pc = pywt.swt(data=self.data, wavelet=self.wavelet, level=1, trim_approx=True)[1]
        else:
            if indexlist[1] % 2 == 1:
                pc = pywt.swt(data=self.getPacketCoefficent([indexlist[0]-1, (indexlist[1] + 1)//2]),
                              wavelet=self.wavelet, level=1, trim_approx=True)[0]
            elif indexlist[1] % 2 ==0:
                pc = pywt.swt(data=self.getPacketCoefficent([indexlist[0] - 1, indexlist[1] // 2]),
                              wavelet=self.wavelet, level=1, trim_approx=True)[1]
        return pc


if __name__ == '__main__':
    t1 = SignalModel.Signal(1000)
    s1 = t1.createSpikeMultiNoise([2, 4, 6])
    sa = pywt.swt(data=s1, wavelet='db3', level=1, trim_approx=True)[0]
    sd = pywt.swt(data=s1, wavelet='db3', level=1, trim_approx=True)[1]
    sda = pywt.swt(data=sd, wavelet='db3', level=1, trim_approx=True)[0]

    sda2 = SWPT(s1).getPacketCoefficent([1, 2])

    plt.figure()
    plt.subplot(2, 1, 1)
    plt.plot([i for i in range(len(sda))], sda)
    plt.subplot(2, 1, 2)
    plt.plot([i for i in range(len(sda2))], sda2)
    plt.show()