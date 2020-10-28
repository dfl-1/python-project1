from GetActualSignal import GetActualSignal
from LayerSelect import LayerSelect
from WtProcess import DWTP
from NoiseDetection import NoiseDetection

if __name__ == '__main__':
    ad = GetActualSignal()
    ad.getwhvalue()
    od1 = ad.selectvalue(start=6000, end=7024)
    dwt = DWTP(od1)
    coeffs = dwt.dwtdec(wtname='db2')
    lsm2 = LayerSelect(od1, 'db2').EntropySelect2()
    lsm1 = LayerSelect(od1, 'db2').WNrecgSelect()
    print(lsm1, lsm2)
