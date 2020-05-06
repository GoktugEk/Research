import numpy as np
import matplotlib.pyplot as plt
import json
import time

def func(x,a,b,c,d,e,f):
    return a*np.exp(-((x-b)/c)**2) + d*np.exp(-((x-e)/f)**2)



with open("results.json") as file:
    pre_results = json.load(file)

keys = pre_results.keys()
keys = list(keys)
pre_results = dict(pre_results)
print(len(keys))

for i in keys:
    popt = pre_results[i]["Parameters"]
    popt = np.array(popt)
    ydata = pre_results[i]["Cases"]
    xdata = range(1,len(ydata)+1)
    xdata = np.array(xdata)
    ydata = np.array(ydata)

    plt.plot(xdata, ydata, 'b-', label=i)
    xdata = range(1,len(ydata)+61)
    plt.plot(xdata, func(xdata, *popt), 'r-', label='Fit')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.savefig("curves_up_to_date/"+str(i)+".png")
    plt.clf()



