from SignalModel import Signal
from LayerSelect import LayerSelect
import matplotlib.pyplot as plt
from WtProcess import DWTP


if __name__ == '__main__':
    s = Signal(1000)
    od1 = s.createSin(50, 60, 4)
    od2 = s.createPulse(50, 60, 4)
    od3 = s.createSpikes(4)
    ods = [od1, od2, od3]
    lssm1 = []
    lssm2 = []
    for od in ods:
        coeffs = DWTP(od).dwtdec('db4')
        lsm1 = LayerSelect(od, 'db4').WNrecgSelect()
        lssm1.append(lsm1)
        lsm2 = LayerSelect(od, 'db4').EntropySelect()
        lssm2.append(lsm2)
    print(lssm1, lssm2)