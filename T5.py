import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import pywt
import csv
import codecs

index = []
n = 1
cn = 1
data = []
with open(r'C:\Users\Jason\Desktop\T2XB.csv', 'r') as f:
    reader = csv.reader(f)
    for i in reader:
        cn += 1
        if 19000 <= cn < 20000:
            data.append(float(i[1]))
            index.append(n)
            n += 1

mintime = 0
maxtime = mintime + len(data) + 1

w = pywt.Wavelet('db2')
maxlev = pywt.dwt_max_level(len(data), w.dec_len)
th = 0.1

coeffs = pywt.wavedec(data, 'db2', level=maxlev)
for i in range(1, len(coeffs)):
    coeffs[i] = pywt.threshold(coeffs[i], th * max(coeffs[i]), mode='garrote')

datarec = pywt.waverec(coeffs, 'db2')

strdata = []
for i in datarec:
    strdata.append(str(i)+"\n")

# f3 = open(r'C:\Users\Jason\Desktop\T2db404g.txt', 'w')
# f3.writelines(strdata)
# f3.close()

# f2 = codecs.open(r'C:\Users\Jason\Desktop\T2XB.csv', 'w', 'utf-8')
# writer = csv.writer(f2)
# for n in strdata:
#     writer.writerow(n)
# f2.close()

plt.figure()
plt.subplot(2,1,1)
plt.plot(index[mintime:maxtime], data[mintime:maxtime])
plt.xlabel('time(s)')

plt.ylabel('intensity')
y_major_locator = MultipleLocator(10000000)
ax = plt.gca()
ax.yaxis.set_major_locator(y_major_locator)
plt.title('Raw Signal')
#
plt.subplot(2,1,2)
plt.plot(index[mintime:maxtime], datarec[mintime:maxtime])
plt.xlabel('time(s)')

plt.ylabel('intensity')
y_major_locator = MultipleLocator(10000000)
ax = plt.gca()
ax.yaxis.set_major_locator(y_major_locator)
plt.title('DeNoised Signal')

plt.tight_layout()
plt.show()
