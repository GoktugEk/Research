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
with open("DATA.txt") as file:
    all_data = file.read().splitlines()
    
    
def func1(x, a, b, c,d,f,g):
    return a**(b*x) + c**(d*x) + f**(g*x)
def func2(x,a,b,c,d,e,f,g):
    return x**b
def func3(x,a,b,c,d,e,f):
    return a*np.exp(-((x-b)/c)**2) + d*np.exp(-((x-e)/f)**2)

functions = {"func1" : "a^(b*x) + c^(d*x) + f^(g*x)", "func2" : "x^b","func3" : "a * e ^ -((x-b)/c)**2 + d * e ^ -((x-e)/f)**2 "}
ydata = []
name = "Aruba"
popt_results = {}
country_names = []
errors = []
daily_case = 4
total_case = 3
total_death = 5


for i in range(len(all_data)):
    country_data = all_data[i].split(",")

    a = random.randrange(5000)
    b = random.randrange(5000)
    c = random.randrange(5000)
    d = random.randrange(5000)
    e = random.randrange(5000)
    f = random.randrange(5000)
    
    if int(country_data[daily_case]) != 0:
        ydata.append(int(country_data[daily_case]))
    
    if i+2 > len(all_data) or all_data[i+1].split(",")[1] != name:
        
        if len(ydata)< 7:
            ydata = []
            name = all_data[i+1].split(",")[1]
            continue
        
        
        xdata = [x for x in range(1,len(ydata)+1)]
        xdata = np.array(xdata)
        ydata = np.array(ydata)
        """
        popt1,pcov1 = curve_fit(func1,xdata,ydata,maxfev = 99999999)
        popt2,pcov2 = curve_fit(func2,xdata,ydata,maxfev = 99999999)
        func1_error = mean_absolute_error(ydata,func1(xdata, *popt1))
        func2_error = mean_absolute_error(ydata,func2(xdata, *popt2))"""
        popt3,pcov3 = curve_fit(func3,xdata,ydata, p0 = [a, b, c, d, e, f],maxfev = 9999999)      
        func3_error = mean_absolute_error(ydata,func3(xdata, *popt3))

        popt3 = popt3.tolist() 
        ydata = ydata.tolist()
        """
        if func2_error >= func1_error  and func3_error  >= func1_error:
            pass
        elif func1_error >= func2_error  and func3_error  >= func2_error:
            pass
        else:"""  
            
        popt_results[name] = {
            "Parameters": popt3, 
            "Function" : functions["func3"], 
            "Cases" : ydata, 
            "Error": func3_error
            }        
                
        ydata = []
        name = all_data[i+1].split(",")[1]
        if name == "$":
            break   
popt_results = json.dumps(popt_results)
print(popt_results)
