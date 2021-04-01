# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 00:32:08 2020

@author: goktu
"""
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import warnings

warnings.simplefilter("ignore")


def clear_zeros(lis):
    for i in range(len(lis)):
        if lis[i] == 0:
            lis[i] = 0.1
        elif str(lis[i]) == 'nan':
            lis[i] = lis[i-1]
    return lis

def func(x,a,b,c,d,e,f):
    return int(a) * x + b * np.square(x) + c + d*np.exp(-((x-e)/f)**2)


df = pd.read_csv("owid-covid-data.csv")

cnts = df.location.unique()


for cnt in cnts:
    cnt_df = df[df["location"] == cnt]

    fts = ['new_cases', 'new_deaths', 'new_tests']
    names = {'new_cases' : 'Case', 'new_deaths' : 'Death', 'new_tests' : 'Test'}
    for ft in fts:
        arr = cnt_df[ft].dropna().to_numpy()
        arr = clear_zeros(arr)

        if len(arr) < 20:
            break

        days = [x for x in range(1, len(arr) + 1)]

        try:
            params,_ = curve_fit(func, days, arr, maxfev=10000000)
        except:
            break
        plt.plot(days, arr, 'b.', label=cnt)
        days = [x for x in range(1, len(arr) + 31)]
        plt.plot(days, func(days, *params), 'r-', label='Fit')
        plt.xlabel('Days Since The First ' + names[ft] + ' Announced')
        plt.ylabel("Number of Daily " + names[ft] + "s")
        plt.legend()
        plt.savefig("../Graphs/Covid-19-Country-Graphs/" + str(ft) + "/" + str(cnt) + ".png")
        plt.clf()


