import pywt
from ThresholdSelect import ThSelect
from ThresholdFunction import ThFuction
import numpy as np


class DWTP:
    def __init__(self, data):
        self.data = data

    def maxdeclevel(self,wtname='db4'):
        w = pywt.Wavelet(wtname)
        maxlev = pywt.dwt_max_level(len(self.data), w.dec_len)
        return maxlev

    def dwtdec(self,wtname='db4',delevel=None):
        w = pywt.Wavelet(wtname)
        if not delevel:
            maxlev = pywt.dwt_max_level(len(self.data), w.dec_len)
            delevel = maxlev
        coeffs = pywt.wavedec(self.data, wtname, level=delevel)
        return coeffs

    def thprocess(self, coeffs, ths=None, thf='soft', thp=None):
        ncoeffs = [coeffs[0]]
        for i in range(1, len(coeffs)):
            if not ths:
                th = ThSelect(coeffs[i]).DonohoThEx()
            elif len(ths) == len(coeffs)-1:
                th = ths[i-1]
            else:
                raise ValueError('number of th in ths[] must match levels of coeffs')
            if thf == 'soft':
                ncf = ThFuction(coeffs[i]).thsoft(th)
            elif thf == 'hard':
                ncf = ThFuction(coeffs[i]).thhard(th)
            elif thf == 'thsemisf':
                ncf = ThFuction(coeffs[i]).thsemisf(th, thp)
            elif thf == 'thf1':
                ncf = ThFuction(coeffs[i]).thf1(th, thp)
            elif thf == 'thf2':
                ncf = ThFuction(coeffs[i]).thf2(th, thp)
            elif thf == 'thf3':
                ncf = ThFuction(coeffs[i]).thf1(th, thp)
            else:
                raise ValueError('thf must be "soft","hard","thsemisf","thf1","thf2","thf3"')
            ncoeffs.append(np.asarray(ncf))
        return ncoeffs

    def thprocess2(self, coeffs, ths=None, thf='soft', thps=None):
        ncoeffs = [coeffs[0]]
        for i in range(1, len(coeffs)):
            if len(ths) == len(coeffs)-1:
                th = ths[i-1]
            else:
                raise ValueError('number of th in ths[] must match levels of coeffs')
            if len(thps) == len(coeffs)-1:
                thp = thps[i-1]
            else:
                raise ValueError('number of th in ths[] must match levels of coeffs')
            if thf == 'thf2':
                ncf = ThFuction(coeffs[i]).thf2(th, thp)
            elif thf == 'thf3':
                ncf = ThFuction(coeffs[i]).thf1(th, thp)
            else:
                raise ValueError('thf must be "thf2","thf3"')
            ncoeffs.append(np.asarray(ncf))
        return ncoeffs

    def dwtrec(self, coffes, wtname='db4'):
        ndata = pywt.waverec(coffes, wtname)
        return ndata


class SWTP:
    def __init__(self, data):
        self.data = data

    def maxdeclevel(self):
        maxlev = pywt.swt_max_level(len(self.data))
        return maxlev

    def swtdec(self, wtname='db4', delevel=None):
        if not delevel:
            delevel = self.maxdeclevel()
        coeffs = pywt.swt(self.data, wtname, level=delevel, trim_approx=True)
        return coeffs

    def thprocess(self, coeffs, ths=None, thf='soft', thp=None):
        ncoeffs = [coeffs[0]]
        for i in range(1, len(coeffs)):
            if not ths:
                th = ThSelect(coeffs[i]).DonohoThEx2(len(coeffs)-i)
            elif len(ths) == len(coeffs)-1:
                th = ths[i-1]
            else:
                raise ValueError('number of th in ths[] must match levels of coeffs')
            if thf == 'soft':
                ncf = ThFuction(coeffs[i]).thsoft(th)
            elif thf == 'hard':
                ncf = ThFuction(coeffs[i]).thhard(th)
            elif thf == 'thsemisf':
                ncf = ThFuction(coeffs[i]).thsemisf(th, thp)
            elif thf == 'thf1':
                ncf = ThFuction(coeffs[i]).thf1(th, thp)
            elif thf == 'thf2':
                ncf = ThFuction(coeffs[i]).thf2(th, thp)
            elif thf == 'thf3':
                ncf = ThFuction(coeffs[i]).thf1(th, thp)
            else:
                raise ValueError('thf must be "soft","hard","thsemisf","thf1","thf2","thf3"')
            ncoeffs.append(np.asarray(ncf))
        return ncoeffs

    def thprocess2(self, coeffs, ths=None, thf='soft', thps=None):
        ncoeffs = [coeffs[0]]
        for i in range(1, len(coeffs)):
            if len(ths) == len(coeffs)-1:
                th = ths[i-1]
            else:
                raise ValueError('number of th in ths[] must match levels of coeffs')
            if len(thps) == len(coeffs)-1:
                thp = thps[i-1]
            else:
                raise ValueError('number of th in ths[] must match levels of coeffs')
            if thf == 'thf2':
                ncf = ThFuction(coeffs[i]).thf2(th, thp)
            elif thf == 'thf3':
                ncf = ThFuction(coeffs[i]).thf1(th, thp)
            else:
                raise ValueError('thf must be "thf2","thf3"')
            ncoeffs.append(np.asarray(ncf))
        return ncoeffs

    def swtrec(self,coffes, wtname='db4'):
        ndata = pywt.iswt(coffes, wtname)
        return ndata




