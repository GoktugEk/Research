#!/bin/bash

wget --output-document=owid-covid-data.csv https://covid.ourworldindata.org/data/owid-covid-data.csv ##

echo -ne "Fitting curves...               \r" ##
python3 curve_fitting.py ##

cd .. ##
cd Covid-19-Country-Graphs/ ##

echo "Pushing changes to Github...             \r" ##
git stage * ##
now=$(date +'%m/%d/%Y') ##
git commit -m "$now" ##
git push ##
echo -ne '###########################(100%)\n'