import numpy as np
import matplotlib.pyplot as plt
import json
import time

def func(x,a,b,c):
    return a*np.exp(-((x-b)/c)**2)

def to_array(lis):
    lis = np.array(lis)

def make_days(num):
    xdata = [x for x in range(1,num+1)]
    return xdata

def get_data(results, index, key):
    ydata = results[index][key]
    return ydata


def plot(xdata, ydata, params, feature,name, days, subkey):
    plt.plot(xdata, ydata, 'b-', label=name)
    xdata = make_days(len(ydata)+days)
    plt.plot(xdata, func(xdata, *params), 'r-', label='Fit')
    plt.xlabel('Days Since The First ' + str(feature) + ' Announced')
    plt.ylabel("Number of Daily "+ feature + "s")
    plt.legend()
    plt.savefig("../Covid-19-Country-Graphs/60_days_"+ str(subkey) + "/"+str(name)+".png")
    plt.clf()




with open("results.json") as file:
    pre_results = json.load(file)

main_keys = [("Daily Cases","Case"), ("Daily Deaths","Death"), ("Daily Tests", "Test")]

for subkey,feature in main_keys:

    keys = pre_results[subkey].keys()
    keys = list(keys)
    results = dict(pre_results[subkey])
    print(subkey + "...")

    for i in keys:
        params = get_data(results,i,"Parameters")
        ydata = get_data(results, i, "Cases")
        length = len(ydata)
        xdata = make_days(length)

        xdata = np.array(xdata)
        ydata = np.array(ydata)
        params = np.array(params)


        plot(xdata,ydata,params,feature,i,60,subkey)
        plot(xdata,ydata,params,feature,i,30,subkey)




