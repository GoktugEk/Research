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





def get_the_data( lis, option): #INPUT : LIST OF DICTIONARIES OF COUNTRY FEATURES
    ydata = []                  #OUTPUT: xdata: array of days, length is equivalent with ydata            
    name = lis[0]["location"]   #        ydata: array of desired feature,
    for i in lis:               #        name: name of the country
        if option in i.keys() and i[option] != 0:
            ydata.append(i[option])

    xdata = [x for x in range(1,len(ydata)+1)]
    xdata = np.array(xdata)
    ydata = np.array(ydata)
    return xdata,ydata,name


def add_the_data(results, feature, popt, ydata, error, name):
    results[feature][name] =  {
                "Parameters": popt, 
                "Cases" : ydata, 
                "Error": error
                }    


def fit_and_error(func, xdata, ydata,init):
    if init:
        popt,_ = curve_fit(func,xdata,ydata, p0 = [0.5, 0.5, 0.5], maxfev = 999999)
    else:
        popt,_ = curve_fit(func,xdata,ydata, p0 = None, maxfev = 999999)
    error  = mean_absolute_error(ydata,func3(xdata, *popt))
    popt = popt.tolist()
    return popt,error
    



with open("owid-covid-data.json") as file:
    pre_results = json.load(file)

keys = pre_results.keys()
keys = list(keys)
results = dict(pre_results)


def func3(x,a,b,c):
    return a*np.exp(-((x-b)/c)**2) 



popt_results = {"Daily Cases" : {}, "Daily Deaths" : {}, "Daily Tests" : {}}
situations = [("new_cases","Daily Cases"),("new_deaths","Daily Deaths"),("new_tests","Daily Tests")]



for case,kind in situations:
    for i in keys:
        occasions = results[i]

        xdata,ydata,name = get_the_data(occasions,case)
        
        if len(ydata) < 20:
            continue


        param1,error1 = fit_and_error(func3,xdata,ydata,0)
        param2,error2 = fit_and_error(func3,xdata,ydata,1)

        

        ydata = ydata.tolist()

        if error1 < error2:
            add_the_data(popt_results,kind, param1, ydata, error1, name)
        else:
            add_the_data(popt_results,kind, param2, ydata, error2, name)


popt_results = json.dumps(popt_results,indent= 4)
print(popt_results)
