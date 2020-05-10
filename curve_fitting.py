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
popt_results = {"Daily Cases" : {}, "Daily Deaths" : {}, "Daily Tests" : {}}
country_names = []
errors = []


total_case = 3
daily_case = 4
total_death = 5
daily_death = 6
daily_tests = 12

situations = [(daily_case,"Daily Cases"),(daily_death,"Daily Deaths"),(daily_tests,"Daily Tests")]
all_data.append("x,$")

for case,kind in situations:
    i = 0 
    while i < len(all_data):

        country_data = all_data[i].split(",")

        a = random.randrange(500)
        b = random.randrange(500)
        c = random.randrange(500)
        d = random.randrange(500)
        e = random.randrange(500)
        f = random.randrange(500)
        
        if country_data[case] != '' and int(float(country_data[case])) != 0:
            ydata.append(int(float(country_data[case])))
        
        if i+2 > len(all_data) or all_data[i+1].split(",")[1] != name:
            

            if len(ydata)< 7 or name == "International" or name == "Jersey":
                ydata = []
                name = all_data[i+1].split(",")[1]
                i+=1
                if name == "$":
                    break
                continue
            
            
            xdata = [x for x in range(1,len(ydata)+1)]
            xdata = np.array(xdata)
            ydata = np.array(ydata)
            """
            popt1,pcov1 = curve_fit(func1,xdata,ydata,maxfev = 99999999)

            func1_error = mean_absolute_error(ydata,func1(xdata, *popt1))
            func2_error = mean_absolute_error(ydata,func2(xdata, *popt2))""" 
            popt3,pcov3 = curve_fit(func3,xdata,ydata, p0 = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5],maxfev = 9999999)  
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
            name = all_data[i+1].split(",")[1]
            if name == "$":
                break   


        i+=1
    

popt_results = json.dumps(popt_results,indent= 4)
print(popt_results)
