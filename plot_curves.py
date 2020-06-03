import numpy as np
import matplotlib.pyplot as plt
import json
import time

# Model function for the curve fitting.
# a,b,c are the parameters, x is the data, type = array
def func(x,a,b,c):
    return a*np.exp(-((x-b)/c)**2)

#INPUT :  num: number of the days equivelent to the ydata, which is the length of the array of cases/tests/deaths, type = int
#RETURN:  xdata: x axis of the graph, type = array
def make_days(num):
    xdata = [x for x in range(1,num+1)]
    return xdata

#INPUT : results: data, type = dict
#      : name: name of the country, type = str
#      : key : the wanted feature e.g cases, parameters ,error. type = str  
def get_data(results, name, key):
    ydata = results[name][key]
    return ydata

#INPUT : xdata   : x axis of the both curves, type = array
#        ydata   : y axis of the real curve, type = array
#        params  : parameters fitted for the function, type = array
#        feature : kind of the data e.g "Case", "Test", "Death", type = str
#        name    : name of the country, type = str
#        days    : number of how many days the prediction curve will continue after real curve finished. type = int
#        subkey  : name for the y axis label e.g Daily Cases, Daily Deaths. type = str
#METHOD: Plots the two curves, which is real curve and the predicted curve by curve fitting.
#        Saves them with the name template <name>.png to the desired path
def plot(xdata, ydata, params, feature,name, days, subkey):
    plt.plot(xdata, ydata, 'b-', label=name)
    xdata = make_days(len(ydata)+days)
    plt.plot(xdata, func(xdata, *params), 'r-', label='Fit')
    plt.xlabel('Days Since The First ' + str(feature) + ' Announced')
    plt.ylabel("Number of Daily "+ feature + "s")
    plt.legend()
    plt.savefig("../Covid-19-Country-Graphs/"+ str(days) +"_days_"+ str(subkey) + "/"+str(name)+".png")
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




