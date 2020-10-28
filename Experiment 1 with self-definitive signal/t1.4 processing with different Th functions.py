from SignalModel import Signal
from LayerSelect import LayerSelect
import matplotlib.pyplot as plt
import numpy as np
from BlockThMethod import BlockThMethod
from ThresholdSelect import ThSelect
from WtProcess import DWTP
from DenoiseResult import DenoiseRsult

if __name__ == '__main__':
    s = Signal(1000)
    od1 = s.createSin(50, 60, 4)
    od2 = s.createPulse(50, 60, 4)
    od3 = s.createSpikes(4)
    ods = [od1, od2, od3]
    spds = []
    hpds = []
    thsemispds = []
    thf1pds = []
    thf2pds = []
    thf3pds = []
    dnames = ['Sine', 'Pulse', 'Spike']
    thfname = ['soft', 'hard', 'thsemisf', 'thf1', 'thf2', 'thf3']
    pdsmatrix = [spds, hpds, thsemispds, thf1pds, thf2pds, thf3pds]
    thps = [None, None, None, 0.5, 2, 2]

    for od in ods:
        dwd = DWTP(od)
        coeffs = dwd.dwtdec(wtname='db4', delevel=2)
        for i in range(len(pdsmatrix)):
            ncoeffs = dwd.thprocess(coeffs, thf=thfname[i], thp=thps[i])
            pd = dwd.dwtrec(ncoeffs, wtname='db4')
            pdsmatrix[i].append(pd)
 
    ssnrs = []
    hsnrs = []
    thsemissnrs = []
    thf1snrs = []
    thf2snrs = []
    thf3snrs = []

    smses = []
    hmses = []
    thsemismses = []
    thf1mses = []
    thf2mses = []
    thf3mses = []

    ssms = []
    hsms = []
    thsemissms = []
    thf1sms = []
    thf2sms = []
    thf3sms = []

    slrepvs = []
    hlrepvs = []
    thsemislrepvs = []
    thf1lrepvs = []
    thf2lrepvs = []
    thf3lrepvs = []
    tds = [s.createSin(50, 60, 0), s.createPulse(50, 60, 0), s.createSpikes(0)]
    for i in range(len(ods)):
        sdr = DenoiseRsult(tds[i], spds[i])
        hdr = DenoiseRsult(tds[i], hpds[i])
        thsemisdr = DenoiseRsult(tds[i], thsemispds[i])
        thf1dr = DenoiseRsult(tds[i], thf1pds[i])
        thf2dr = DenoiseRsult(tds[i], thf2pds[i])
        thf3dr = DenoiseRsult(tds[i], thf3pds[i])
        ssnrs.append(sdr.snr())
        hsnrs.append(hdr.snr())
        thsemissnrs.append(thsemisdr.snr())
        thf1snrs.append(thf1dr.snr())
        thf2snrs.append(thf2dr.snr())
        thf3snrs.append(thf3dr.snr())

        smses.append(sdr.mse())
        hmses.append(hdr.mse())
        thsemismses.append(thsemisdr.mse())
        thf1mses.append(thf1dr.mse())
        thf2mses.append(thf2dr.mse())
        thf3mses.append(thf3dr.mse())

        ssms.append(sdr.smooth(ods[i]))
        hsms.append(hdr.smooth(ods[i]))
        thsemissms.append(thsemisdr.smooth(ods[i]))
        thf1sms.append(thf1dr.smooth(ods[i]))
        thf2sms.append(thf2dr.smooth(ods[i]))
        thf3sms.append(thf3dr.smooth(ods[i]))

        slrepvs.append(sdr.lrepv(ods[i], 100))
        hlrepvs.append(hdr.lrepv(ods[i], 100))
        thsemislrepvs.append(thsemisdr.lrepv(ods[i], 100))
        thf1lrepvs.append(thf1dr.lrepv(ods[i], 100))
        thf2lrepvs.append(thf2dr.lrepv(ods[i], 100))
        thf3lrepvs.append(thf3dr.lrepv(ods[i], 100))

    snrss = [ssnrs, hsnrs, thsemissnrs, thf1snrs, thf2snrs, thf3snrs]
    snrsn = ['ssnrs', 'hsnrs', 'thsemissnrs', 'thf1snrs', 'thf2snrs', 'thf3snrs']
    msess = [smses, hmses, thsemismses, thf1mses, thf2mses, thf3mses]
    msesn = ['smses', 'hmses', 'thsemismses', 'thf1mses', 'thf2mses', 'thf3mses']

    sms = [ssms, hsms, thsemissms, thf1sms, thf2sms, thf3sms]
    smsn = ['ssms', 'hsms', 'thsemissms', 'thf1sms', 'thf2sms', 'thf3sms']
    lrepvs = [slrepvs, hlrepvs, thsemislrepvs, thf1lrepvs, thf2lrepvs, thf3lrepvs]
    lrepvsn = ['slrepvs', 'hlrepvs', 'thsemislrepvs', 'thf1lrepvs', 'thf2lrepvs', 'thf3lrepvs']
    for i in range(len(snrss)):
        print('{0} = {1}'.format(snrsn[i], snrss[i]))
    print()
    for i in range(len(msess)):
        print('{0} = {1}'.format(msesn[i], msess[i]))
    print()
    for i in range(len(msess)):
        print('{0} = {1}'.format(smsn[i], sms[i]))
    print()
    for i in range(len(msess)):
        print('{0} = {1}'.format(lrepvsn[i], lrepvs[i]))

    x = [x for x in range(1000)]
    for j in range(3):
        plt.figure()
        for i in range(6):
            plt.subplot(3, 2, i+1)
            plt.title('{0} signal by {1} threshold'.format(dnames[j], thfname[i]))
            plt.plot(x, pdsmatrix[i][j])
        plt.tight_layout()
        plt.show()




