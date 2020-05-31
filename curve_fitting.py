# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 00:32:08 2020

@author: goktu
"""
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
from sklearn.cluster import KMeans,estimate_bandwidth
from sklearn.datasets import make_blobs
from sklearn.impute import SimpleImputer
import json
import random


with open("owid-covid-data.json") as file:
    pre_results = json.load(file)

keys = pre_results.keys()
keys = list(keys)
results = dict(pre_results)


def func3(x,a,b,c):
    return a*np.exp(-((x-b)/c)**2) 


functions = {"func1" : "a^(b*x) + c^(d*x) + f^(g*x)", "func2" : "x^b","func3" : "a * e ^ -((x-b)/c)**2 + d * e ^ -((x-e)/f)**2 "}
ydata = []
name = "Aruba"
popt_results = {"Daily Cases" : {}, "Daily Deaths" : {}, "Daily Tests" : {}}
country_names = []
errors = []


total_case = 3
daily_case = 4
total_death = 5
daily_death = 6
daily_tests = 12

situations = [("new_tests","Daily Tests"),("new_cases","Daily Cases"),("new_deaths","Daily Deaths")]



for case,kind in situations:

    for i in keys:
        occasions = results[i]
        for j in occasions:
            if not (case in j.keys()):
                continue
            number = j[case]
            if number != 0:
                ydata.append(int(number))

        name = results[i][0]["location"]
        
        if len(ydata) < 10:
            ydata = []
            continue

        xdata = [x for x in range(1,len(ydata)+1)]
        xdata = np.array(xdata)
        ydata = np.array(ydata)

        popt3,pcov3 = curve_fit(func3,xdata,ydata, p0 = [0.5, 0.5, 0.5],maxfev = 9999999 )  
        popt2,pcov2 = curve_fit(func3,xdata,ydata,p0= None,maxfev = 99999999) 
        error_1 = mean_absolute_error(ydata,func3(xdata, *popt3))
        error_2 = mean_absolute_error(ydata,func3(xdata, *popt2))
        
        popt3 = popt3.tolist()
        popt2 = popt2.tolist()
        ydata = ydata.tolist()

        if error_1 < error_2:
            popt_results[kind][name] = {
                "Parameters": popt3, 
                "Function" : functions["func3"], 
                "Cases" : ydata, 
                "Error": error_1
                }    
        else:
            popt_results[kind][name] = {
                "Parameters": popt2, 
                "Function" : functions["func3"], 
                "Cases" : ydata, 
                "Error": error_2
                }  
        ydata = []
    
        



    

popt_results = json.dumps(popt_results,indent= 4)
print(popt_results)
