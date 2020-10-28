import pywt
import math as mt
import numpy as np
import SignalModel
import matplotlib.pyplot as plt

t1 = SignalModel.Signal(1000)
s1 = t1.createSpikeMultiNoise([2, 4, 6])
wp = pywt.WaveletPacket(data=s1, wavelet='db3')
coeffs = pywt.wavedec(data=s1, wavelet='db3', level=1)
a = coeffs[0]
d = coeffs[1]
aa = pywt.wavedec(data=a, wavelet='db3', level=1)[0]
ad = pywt.wavedec(data=a, wavelet='db3', level=1)[1]
da = pywt.wavedec(data=d, wavelet='db3', level=1)[0]
dd = pywt.wavedec(data=d, wavelet='db3', level=1)[1]
print(dd == wp['dd'].data)

sa = pywt.swt(data=s1, wavelet='db3', level=1, trim_approx=True)[0]
sd = pywt.swt(data=s1, wavelet='db3', level=1, trim_approx=True)[1]
sda = pywt.swt(data=sd, wavelet='db3', level=1, trim_approx=True)[0]

plt.figure()
plt.subplot(2,1,1)
plt.plot([i for i in range(len(da))], da)
plt.subplot(2, 1, 2)
plt.plot([i for i in range(len(sda))], sda)
plt.show()