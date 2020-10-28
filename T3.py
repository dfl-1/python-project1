from array import array

import pywt

# print(help(pywt.threshold))

coffes = pywt.swt([1,2,4,5,6,8,9,4],'db2',level=2,trim_approx=True)
print(coffes)
data = pywt.iswt(coffes,'db2')
print(data)
coffes2=pywt.wavedec([1,2,4,5,6,8,9,4,5,7,6,8,9,10],'db1',level=2)
print(coffes2)
data2=pywt.waverec(coffes2,'db1')
print(data2)
# data3=pywt.waverec(coffes3,'db2')
# print(data3)
# coffes2 = pywt.wavedec([1,2,4,5,6,8,9,4,6],'db1', level=2)
# print(coffes2)
# coffes3 = pywt.wavedec([1,2,4,5,6,8,9,4,6],'db1', level=3)
# print(coffes3)
# w = pywt.Wavelet('db4')
# maxlev = pywt.dwt_max_level(16, w.dec_len)
# print(maxlev)
#
# coffes = pywt.wavedec([1,2,3,4,5],'db1',level=2)
# print(coffes)
# coffes2 = pywt.wavedec([1,2,3,4,5,6,7,8,9,10],'db1',level=3)
# print(coffes2)
# print(pywt.Wavelet('db1').dec_len)