import numpy as np
import json
import header as h
from sklearn.cluster import KMeans,estimate_bandwidth
from sklearn import metrics 
from scipy.spatial.distance import cdist 
import numpy as np 
import matplotlib.pyplot as plt 

clusterings = {}

with open("features.json","r") as f:
    pre_results = json.load(f)


features = pre_results["features"]

for i in range(len(features)-1):
    features[i] = np.array(features[i]) 

features = np.array(features)

names = pre_results["names"]


h.ebw_method(features)

 
kmeans = KMeans(n_clusters=4)
kmeans.fit(features)
labels = kmeans.labels_
label_uniques = np.unique(labels)

clusterings["features"] = pre_results["feature_choices"]
for i in label_uniques:
    clusterings["Cluster " + str(i)] = []

    for j in range(len(labels)-1):
        if labels[j] == i:
            clusterings["Cluster " + str(i)].append(names[j])


clusterings = json.dumps(clusterings,indent=4)
print(clusterings)


 