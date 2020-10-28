import pywt
import matplotlib.pyplot as plt

[phi, psi, x] = pywt.Wavelet('db4').wavefun(1)
plt.figure()
plt.subplot(2,1,1)
plt.plot(x,phi)
plt.subplot(2,1,2)
plt.plot(x,psi)
plt.show()

# print(pywt.wavelist('db'))