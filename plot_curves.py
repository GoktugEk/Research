import numpy as np
import matplotlib.pyplot as plt
import json
import time
import header as h
from header import func






with open("results.json") as file:
    pre_results = json.load(file)

main_keys = [("Daily Cases","Case"), ("Daily Deaths","Death"), ("Daily Tests", "Test")]

for subkey,feature in main_keys:

    keys = pre_results[subkey].keys()
    keys = list(keys)
    results = dict(pre_results[subkey])
    print(subkey + "...")

    for i in keys:
        params = h.get_data(results,i,"Parameters")
        ydata = h.get_data(results, i, "Cases")
        length = len(ydata)
        xdata = h.make_days(length)

        xdata = np.array(xdata)
        ydata = np.array(ydata)
        params = np.array(params)


        h.plot(xdata,ydata,params,feature,i,60,subkey)
        h.plot(xdata,ydata,params,feature,i,30,subkey)




