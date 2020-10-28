import matplotlib.pyplot as plt
import pywt

ecg = pywt.data.ecg()
index = []
data = []
for i in range(len(ecg)-1):
    X = float(i)
    Y = float(ecg[i])
    index.append(X)
    data.append(Y)

w = pywt.Wavelet('db8')
maxlev = pywt.dwt_max_level(len(data), w.dec_len)
th = 0.05

coeffs = pywt.wavedec(data, 'db8', level=maxlev)
for i in range(1, len(coeffs)):
    coeffs[i] = pywt.threshold(coeffs[i], th*max(coeffs[i]))

datarec = pywt.waverec(coeffs, 'db8')

mintime = 0
maxtime = mintime+len(data)+1

plt.figure()
plt.subplot(2,1,1)
plt.plot(index[mintime:maxtime], data[mintime:maxtime])
plt.xlabel('time(s)')
plt.ylabel('microvolts(uV)')
plt.title('Raw Signal')
plt.subplot(2,1,2)
plt.plot(index[mintime:maxtime], datarec[mintime:maxtime-1])
plt.xlabel('time(s)')
plt.ylabel('microvolots (uV)')
plt.title('De-noised Signal')

plt.tight_layout()
plt.show()