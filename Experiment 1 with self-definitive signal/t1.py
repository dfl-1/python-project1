from SignalModel import Signal
import matplotlib.pyplot as plt
from DenoiseResult import DenoiseRsult

s = Signal(1000)
td1 = s.createSin(50, 60, 0)
od1 = s.createSin(50, 60, 4)
td2 = s.createPulse(50, 60, 0)
od2 = s.createPulse(50, 60, 4)
td3 = s.createSpikes(0)
od3 = s.createSpikes(4)

x = [x for x in range(1000)]
plt.figure()
plt.subplot(3, 2, 1)
plt.plot(x, td1)
plt.title("True sine signal")
plt.subplot(3, 2, 2)
plt.plot(x, od1)
plt.title("Noisy sine signal")
plt.subplot(3, 2, 3)
plt.plot(x, td2)
plt.title("True pulse signal")
plt.subplot(3, 2, 4)
plt.plot(x, od2)
plt.title("Noisy pulse signal")
plt.subplot(3, 2, 5)
plt.plot(x, td3)
plt.title("True spike signal")
plt.subplot(3, 2, 6)
plt.plot(x, od3)
plt.title("Noisy spike signal")

dn1 = DenoiseRsult(td1, od1)
dn2 = DenoiseRsult(td2, od2)
dn3 = DenoiseRsult(td3, od3)
print(dn1.snr(), dn2.snr(), dn3.snr())

plt.tight_layout()
plt.show()


