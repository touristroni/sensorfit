import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def func(X, a, b, c):
    t, ts_event, previousfit = X
    return a * np.power((t - ts_event), b) * np.exp(-(t - ts_event) / c) + previousfit


df = pd.read_csv('gekasfit.csv')
color=plt.cm.rainbow(np.linspace(0,1,15))
#initial parameters just dummy
localtime = df['Times']
poptall = [[1,1,1]]


#Events Loop

for e in range(2, 11):

    localtime = df[df.cumul_curve == e]['Times']
    previousfit = [0 for x in localtime]
    if e > 2:
        for p in range(2,e):
            ts_eventold = df[df.cumul_curve == p]['Times'].iloc[0]
            popttemp = poptall[p - 1]

            previousfit = func((localtime,ts_eventold, previousfit),
                               popttemp[0], popttemp[1], popttemp[2])

    ts_event = df[df.cumul_curve == e]['Times'].iloc[0]
    plt.plot(localtime, df[df.cumul_curve == e]['PA3841_dP_cor'], 'b-',
             label='data')# + str(e) )
    popt, pcov = curve_fit(func, (localtime,ts_event, previousfit), df[df.cumul_curve == e]['PA3841_dP_cor'],
                       bounds=([10, 0, 1000], [100., 1., 3000.]))
    print "Event " + str(e) + " parameters : " + str(popt)
    poptall.append(popt)
    res = func((localtime,ts_event, previousfit), popt[0], popt[1], popt[2])
    plt.plot(localtime, res, 'r-', label='fit Event ' + str(e),c= color[e])

#plt.legend()
plt.show()