import matplotlib.pyplot as plt
import numpy as np
import math as mt
import pywt

x = np.arange(200)
y = np.sin(2*np.pi*x/32)
y2 = 10*mt.e**(-(x-100)**2/0.5)
coef, freqs = pywt.cwt(y2, np.arange(1, 129), 'gaus1')
plt.matshow(coef)
plt.show()