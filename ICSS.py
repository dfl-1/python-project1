import pywt
import math as mt
import numpy as np
import SignalModel

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