from SignalModel import Signal
import matplotlib.pyplot as plt
from WtProcess import DWTP

if __name__ == '__main__':
    s = Signal(1000)
    od1 = s.createSin(50, 60, 4)
    od2 = s.createPulse(50, 60, 4)
    od3 = s.createSpikes(4)
    ods = [od1, od2, od3]
    cfss =[]
    for od in ods:
        coeffs = DWTP(od).dwtdec('db4',delevel=3)
        cfss.append(coeffs)

    for i in range(1, 4):
        x = [x for x in range(len(cfss[0][-i]))]
        plt.figure()
        plt.subplot(3, 1, 1)
        plt.title('Sine signal d{0} coefficient'.format(i))
        plt.plot(x, cfss[0][-i])

        plt.subplot(3, 1, 2)
        plt.title('Pulse signal d{0} coefficient'.format(i))
        plt.plot(x, cfss[1][-i])

        plt.subplot(3, 1, 3)
        plt.title('Spike signal d{0} coefficient'.format(i))
        plt.plot(x, cfss[2][-i])
        plt.tight_layout()
        plt.show()