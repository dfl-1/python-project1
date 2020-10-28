from SignalModel import Signal
import matplotlib.pyplot as plt
from WtProcess import SWTP
from SpatialCorrelationThresholdALG import SpCoThALG
from ThSearchAlgorithm import ThSearchAlgorithm
from ThresholdSelect import ThSelect
from DenoiseResult import DenoiseRsult

if __name__ == '__main__':
    s = Signal(1024)
    od1 = s.createSin(50, 60, 4)
    od2 = s.createPulse(50, 60, 4)
    od3 = s.createSpikes(4)
    ods = [od1, od2, od3]
    dnames = ['Sine', 'Pulse', 'Spike']
    sf1pds = []
    sf2pds = []
    sfp1pds = []
    sfp2pds = []

    for od in ods:
        swt = SWTP(od)
        coeffs = swt.swtdec(wtname='sym6', delevel=4)
        spta = SpCoThALG(coeffs)
        nce1s = spta.spcoThf1()
        nce2s = spta.spcoThf2()
        sf1pd = swt.swtrec(nce1s, wtname='sym6')
        sf2pd = swt.swtrec(nce2s, wtname='sym6')
        sf1pds.append(sf1pd)
        sf2pds.append(sf2pd)

    for od in ods:
        swt = SWTP(od)
        coeffs = swt.swtdec(wtname='sym6', delevel=4)
        spta2 = SpCoThALG(coeffs)
        sfp1ths = []
        sfp2ths = []
        P = spta2.spcoCors()
        for i in range(1, len(coeffs)-1):
            spta2.BTHassitIndex(i, pk=0.1, pa=4, mode='srmse')
            gpth = ThSelect(P[i-1]).DonohoThEx()
            sfp1th = ThSearchAlgorithm().FibonacciSearch(spta2.BTHspcothfwp1, [0, 1.5*gpth], 0.001)
            sfp2th = ThSearchAlgorithm().FibonacciSearch(spta2.BTHspcothfwp2, [0, 1.5*gpth], 0.001)
            sfp1ths.append(sfp1th)
            sfp2ths.append(sfp2th)
        npce1s = spta2.spcoThfwp1(sfp1ths, 0.05)
        npce2s = spta2.spcoThfwp2(sfp2ths, 4)
        sfp1pd = swt.swtrec(npce1s, wtname='sym6')
        sfp2pd = swt.swtrec(npce2s, wtname='sym6')
        sfp1pds.append(sfp1pd)
        sfp2pds.append(sfp2pd)

    sf1snrs = []
    sf2snrs = []
    sfwp1snrs = []
    sfwp2snrs = []

    sf1mses = []
    sf2mses = []
    sfwp1mses = []
    sfwp2mses = []
    tds = [s.createSin(50, 60, 0), s.createPulse(50, 60, 0), s.createSpikes(0)]
    for i in range(len(tds)):
        sf1dr = DenoiseRsult(tds[i], sf1pds[i])
        sf2dr = DenoiseRsult(tds[i], sf2pds[i])
        sfwp1dr = DenoiseRsult(tds[i], sfp1pds[i])
        sfwp2dr = DenoiseRsult(tds[i], sfp2pds[i])
        sf1snrs.append(sf1dr.snr())
        sf2snrs.append(sf2dr.snr())
        sfwp1snrs.append(sfwp1dr.snr())
        sfwp2snrs.append(sfwp2dr.snr())

        sf1mses.append(sf1dr.mse())
        sf2mses.append(sf2dr.mse())
        sfwp1mses.append(sfwp1dr.mse())
        sfwp2mses.append(sfwp2dr.mse())
        
    snrss = [sf1snrs, sf2snrs, sfwp1snrs, sfwp2snrs]
    snrsn = ['sf1snrs', 'sf2snrs', 'sfwp1snrs', 'sfwp2snrs']
    msess = [sf1mses, sf2mses, sfwp1mses, sfwp2mses]
    msesn = ['sf1mses', 'sf2mses', 'sfwp1mses', 'sfwp2mses']
    for i in range(len(snrss)):
        print('{0} = {1}'.format(snrsn[i], snrss[i]))
    print()
    for i in range(len(msess)):
        print('{0} = {1}'.format(msesn[i], msess[i]))

    x = [x for x in range(1024)]
    plt.figure()
    for i in range(len(ods)):
        plt.subplot(3, 2, 2 * i + 1)
        plt.title('{0} original signal'.format(dnames[i]))
        plt.plot(x, ods[i])
        plt.subplot(3, 2, 2 * i + 2)
        plt.title('{0} signal processed by spthf1'.format(dnames[i]))
        plt.plot(x, sf1pds[i])
    plt.tight_layout()

    plt.figure()
    for i in range(len(ods)):
        plt.subplot(3, 2, 2 * i + 1)
        plt.title('{0} original signal'.format(dnames[i]))
        plt.plot(x, ods[i])
        plt.subplot(3, 2, 2 * i + 2)
        plt.title('{0} signal processed by spthf2'.format(dnames[i]))
        plt.plot(x, sf2pds[i])
    plt.tight_layout()

    plt.figure()
    for i in range(len(ods)):
        plt.subplot(3, 2, 2 * i + 1)
        plt.title('{0} original signal'.format(dnames[i]))
        plt.plot(x, ods[i])
        plt.subplot(3, 2, 2 * i + 2)
        plt.title('{0} signal processed by spwpthf2'.format(dnames[i]))
        plt.plot(x, sfp2pds[i])
    plt.tight_layout()
    plt.show()


