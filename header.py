from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import json
from sklearn.cluster import KMeans,estimate_bandwidth
from sklearn import metrics 
from scipy.spatial.distance import cdist 





#INPUT : LIST OF DICTIONARIES OF COUNTRY FEATURES
#OUTPUT: 
#        ydata: array of desired feature,
#        name: name of the country, type = str
def get_the_data( dct, key,feature): 
    ydata = []     
    lis = dct[key]["data"]                         
    name = dct[key]["location"]  
    if feature in dct[key].keys():
        return [dct[key][feature]],name 
    for i in lis:               
        if feature in i.keys() and i[feature] != 0:
            ydata.append(i[feature])
    return ydata,name

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
    

# Model function for the curve fitting.
# a,b,c are the parameters, x is the data, type = array
def func(x,a,b,c):
    return a*np.exp(-((x-b)/c)**2) 

#INPUT :  num: length of desired list
#RETURN:  xdata: x axis of the graph, type = list
#METHOD:  returns a list starts from 1 to num+1
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


#INPUT: list of numbers
#RETURN: average of numbers where the last numbers have more weight in average
def average(l):
    if l[-1] == -1:
        return -1
    length = 0
    sum = 0
    mltp = 1
    for i in l:
        sum += float(i)*mltp
        length += mltp
        mltp += 0.2
    return sum/length


#INPUT : array of features
#OUTPUT: graph of distortion and inertia of algorithm KMeans
#Method: Elbow Method
def ebw_method(features):
    distortions = [] 
    inertias = [] 
    mapping1 = {} 
    mapping2 = {} 
    K = range(1,10)

    for k in K:
        kmodel = KMeans(n_clusters=k).fit(features)
        kmodel.fit(features)

        dist = sum(np.min(cdist(features, kmodel.cluster_centers_,'euclidean'), axis=1)) / features.shape[0]

        distortions.append(dist)
        inertias.append(kmodel.inertia_)

        mapping1[k] = dist
        mapping2[k] = kmodel.inertia_


    plt.plot(K, distortions, 'bx-') 
    plt.xlabel('Values of K') 
    plt.ylabel('Distortion') 
    plt.title('The Elbow Method using Distortion') 
    plt.show() 

    plt.clf()


    plt.plot(K, inertias, 'bx-') 
    plt.xlabel('Values of K') 
    plt.ylabel('Inertia') 
    plt.title('The Elbow Method using Inertia') 
    plt.show()  


# INPUT : str
# OUTPUT: str with "(-1)" at the end
# If str already has (-1) at the end it does nothing
def add_1(name):
    name = name.rstrip("(-1)")
    name += "(-1)" 
    return name

