# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 00:32:08 2020

@author: goktu
"""
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import json
import warnings
from header import func
import header as h

warnings.simplefilter("ignore")



with open("owid-covid-data.json") as file:
    pre_results = json.load(file)

keys = pre_results.keys()
keys = list(keys)
results = dict(pre_results)


popt_results = {"Daily Cases" : {}, "Daily Deaths" : {}, "Daily Tests" : {}}
main_keys = [("new_cases","Daily Cases"),("new_deaths","Daily Deaths"),("new_tests","Daily Tests")]



for case,kind in main_keys:

    for i in keys:
            
        ydata,name = h.get_the_data(results, i,case)
        
        xdata = h.make_days(len(ydata))

        xdata = np.array(xdata)
        ydata = np.array(ydata)
        
        if len(ydata) < 20:
            continue


        param1,error1 = h.fit_and_error(func,xdata,ydata,0)
        param2,error2 = h.fit_and_error(func,xdata,ydata,1)

        

        ydata = ydata.tolist()

        if error1 < error2:
            h.add_the_data(popt_results,kind, param1, ydata, error1, name)
        else:
            h.add_the_data(popt_results,kind, param2, ydata, error2, name)


popt_results = json.dumps(popt_results,indent= 4)
print(popt_results)
