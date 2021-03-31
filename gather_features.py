import numpy as np
import json
import header as h


features = (("hospital_beds_per_thousand",0),("handwashing_facilities",0),("median_age",0),("aged_65_older",0),("stringency_index",1))
features_2 = (("median_age",0),("aged_65_older",0),("gdp_per_capita",0),("extreme_poverty",0),\
    ("diabetes_prevalence",0),("male_smokers",0),("female_smokers",0),("population_density",0))


ft_cvd_related = (("cvd_death_rate",0),("cvd_death_rate",0))

feature_results = {"features" : [],"names" : [], "feature_choices" : []}

with open("owid-covid-data.json") as file:
    pre_results = json.load(file)

keys = pre_results.keys()
keys = list(keys)
results = dict(pre_results)
temp = []


for i in keys:
    country = results[i]
    feats = []

    for feature,par in ft_cvd_related:

        ydata,name = h.get_the_data(results,i,feature)


        if ydata[-1]  == -1:
            name = h.add_1(name)


        if par == 0:
            feats.append(ydata[-1])

        else:
            avg = h.average(ydata) 
            feats.append(avg)

        if not(feature in feature_results["feature_choices"]):
            feature_results["feature_choices"].append(feature)
    
    feature_results["features"].append(feats)
    feature_results["names"].append(name)


feature_results = json.dumps(feature_results,indent=4)
print(feature_results)
