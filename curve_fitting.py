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
import warnings
warnings.simplefilter("ignore")

#INPUT : LIST OF DICTIONARIES OF COUNTRY FEATURES
#OUTPUT: xdata: array of days, length is equivalent with ydata
#        ydata: array of desired feature,
#        name: name of the country, type = str
def get_the_data( lis, option): 
    ydata = []                              
    name = lis[0]["location"]   
    for i in lis:               
        if option in i.keys() and i[option] != 0:
            ydata.append(i[option])

    xdata = [x for x in range(1,len(ydata)+1)]
    xdata = np.array(xdata)
    ydata = np.array(ydata)
    return xdata,ydata,name

#INPUT: results: Dict has the keys of 3 main keys
#       feature: The name of the occasion e.g Daily case, Daily Death, Type = str
#       popt   : Parameters of the fit, type = array
#       ydata  : Cases of the country, can be deaths, tests or cases, type = array
#       error  : Error calculated between fitted curve and original curve, type = array
#METHOD: Adds the given data to the results dictionary under feature key   
def add_the_data(results, feature, popt, ydata, error, name):
    results[feature][name] =  {
                "Parameters": popt, 
                "Cases" : ydata, 
                "Error": error
                }    

#INPUT:  func  : Function will be used for curve fitting
#        xdata : x axis of the graph, type = array
#        ydata : cases of the country, type = array
#        init  : Variable decides whether curve fit used with initalized parameters or not. 1 = init, 0 = regular
#RETURN: popt  : Parameters fitted to the function by curve fit function
#        error : Error calculated between fitted curve and original curve
#METHOD: Calculates fitted parameters and errors with the functions curve_fit and mean_absolute_error, returns the output
def fit_and_error(func, xdata, ydata,init):
    if init:
        popt,_ = curve_fit(func,xdata,ydata, p0 = [0.5, 0.5, 0.5], maxfev = 999999)
    else:
        popt,_ = curve_fit(func,xdata,ydata, p0 = None, maxfev = 999999)
    error  = mean_absolute_error(ydata,func(xdata, *popt))
    popt = popt.tolist()
    return popt,error
    



with open("owid-covid-data.json") as file:
    pre_results = json.load(file)

keys = pre_results.keys()
keys = list(keys)
results = dict(pre_results)


# Model function for the curve fitting.
# a,b,c are the parameters, x is the data, type = array
def func(x,a,b,c):
    return a*np.exp(-((x-b)/c)**2) 



popt_results = {"Daily Cases" : {}, "Daily Deaths" : {}, "Daily Tests" : {}}
main_keys = [("new_cases","Daily Cases"),("new_deaths","Daily Deaths"),("new_tests","Daily Tests")]



for case,kind in main_keys:

    for i in keys:
        occasions = results[i]

        xdata,ydata,name = get_the_data(occasions,case)
        
        if len(ydata) < 20:
            continue


        param1,error1 = fit_and_error(func,xdata,ydata,0)
        param2,error2 = fit_and_error(func,xdata,ydata,1)

        

        ydata = ydata.tolist()

        if error1 < error2:
            add_the_data(popt_results,kind, param1, ydata, error1, name)
        else:
            add_the_data(popt_results,kind, param2, ydata, error2, name)


popt_results = json.dumps(popt_results,indent= 4)
print(popt_results)
