import numpy as np
import matplotlib.pyplot as plt
import json
import time

def func(x,a,b,c):
    return a*np.exp(-((x-b)/c)**2)



with open("results.json") as file:
    pre_results = json.load(file)

main_keys = [("Daily Cases","Case"), ("Daily Deaths","Death"), ("Daily Tests", "Test")]
for kind,happen in main_keys:

    keys = pre_results[kind].keys()
    keys = list(keys)
    results = dict(pre_results[kind])
    print(len(keys))

    for i in keys:
        popt = results[i]["Parameters"]
        popt = np.array(popt)
        ydata = results[i]["Cases"]
        xdata = range(1,len(ydata)+1)
        backup_x = range(1,len(ydata)+1)
        xdata = np.array(xdata)
        ydata = np.array(ydata)

        plt.plot(xdata, ydata, 'b-', label=i)
        xdata = range(1,len(ydata)+61)
        plt.plot(xdata, func(xdata, *popt), 'r-', label='Fit')
        plt.xlabel('Days Since The First ' + str(happen) + ' Announced')
        plt.ylabel("Number of Daily "+ happen + "s")
        plt.legend()
        plt.savefig("../Covid-19-Country-Graphs/60_days_"+ str(kind) + "/"+str(i)+".png")
        plt.clf()
        xdata = range(1,len(ydata)+31)
        plt.plot(backup_x, ydata, 'b-', label=i)
        plt.plot(xdata, func(xdata, *popt), 'r-', label='Fit')
        plt.xlabel('Days Since The First ' + str(happen) + ' Announced')
        plt.ylabel("Number of Daily "+ happen + "s")
        plt.legend()
        plt.savefig("../Covid-19-Country-Graphs/60_days_"+ str(kind) + "/"+str(i)+".png")
        plt.clf()



