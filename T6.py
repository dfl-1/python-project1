import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import pywt
import csv
from math1 import gt
import codecs

index = []
n = 1
cn = 1
data = []
with open(r'C:\Users\Jason\Desktop\T2XB.csv', 'r') as f:
    reader = csv.reader(f)
    for i in reader:
        cn += 1
        if 22500 <= cn < 23000:
            data.append(float(i[1]))
            index.append(n)
            n += 1

mintime = 0
maxtime = mintime + len(data) + 1
w = pywt.Wavelet('db2')
coeffs = pywt.wavedec(data, 'db2', level=3)

lc1=len(coeffs[3])
lc2=len(coeffs[2])
print(lc1,lc2)

cf = list(coeffs[3]**2)
cf2=gt(list(coeffs[3])).gtan(1)

datarec = pywt.waverec(coeffs, 'db2')


plt.figure()
plt.subplot(4,1,1)
plt.plot(index[mintime:maxtime], data[mintime:maxtime])
plt.xlabel('time(s)')

plt.ylabel('intensity')
y_major_locator = MultipleLocator(10000000)
ax = plt.gca()
ax.yaxis.set_major_locator(y_major_locator)
plt.title('Raw Signal')

plt.subplot(4,1,2)
plt.plot(index[mintime:maxtime], datarec[mintime:maxtime])
plt.xlabel('time(s)')

plt.ylabel('intensity')
y_major_locator = MultipleLocator(10000000)
ax = plt.gca()
ax.yaxis.set_major_locator(y_major_locator)
plt.title('DeNoised Signal')

plt.subplot(4,1,3)
plt.plot(index[mintime:lc1], coeffs[3][mintime:lc1])
plt.xlabel('time(s)')

plt.ylabel('intensity')
y_major_locator = MultipleLocator(10000000)
ax = plt.gca()
ax.yaxis.set_major_locator(y_major_locator)
plt.title('wavelet coeffs1')

plt.subplot(4,1,4)
plt.plot(index[mintime:len(cf)], cf[mintime:len(cf)])
plt.xlabel('time(s)')

plt.ylabel('intensity')
y_major_locator = MultipleLocator(10000000)
ax = plt.gca()
ax.yaxis.set_major_locator(y_major_locator)
plt.title('wavelet coeffs2')

plt.tight_layout()
plt.show()