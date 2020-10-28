from GetActualSignal import GetActualSignal
from LayerSelect import LayerSelect
from WtProcess import DWTP
from NoiseDetection import NoiseDetection

if __name__ == '__main__':
    ad = GetActualSignal()
    ad.getwhvalue()
    od1 = ad.selectvalue(start=4000, end=5024)
    dwt = DWTP(od1)
    coeffs = dwt.dwtdec(wtname='db2')
    ps1 = NoiseDetection(od1, 'db2').WNrecgmethod()
    ps2 = NoiseDetection(od1, 'db2').Entropymethod1(4)
    print(ps1)
    print(ps2)