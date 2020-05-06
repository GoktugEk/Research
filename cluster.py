from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
from sklearn.cluster import KMeans,estimate_bandwidth
from sklearn import preprocessing
import json

with open("death_cases.json") as file:
    pre_results = json.load(file)
results = pre_results.values()
results = list(results)
results = np.array(results)
names = pre_results.keys()
names = list(names)

cluster_six = [14, 27, 28, 38, 39, 41, 42, 51, 57, 64, 93, 94, 95, 101, 105, 109, 141, 147]

data = preprocessing.StandardScaler()

data.fit(results)

data = data.transform(results)




print(data)

kmeans = KMeans( random_state=0,tol= 0.0000000000000001).fit(data)

labels = kmeans.labels_
cluster_centers = kmeans.cluster_centers_

labels_unique = np.unique(labels)
nclusters = len(labels_unique)


for i in cluster_six:
    print(names[i])
    print(data[i])

print(labels)
print("number of estimated clusters : %d" % nclusters)