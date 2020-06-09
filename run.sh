#!/bin/bash

wget --output-document=owid-covid-data.json https://covid.ourworldindata.org/data/owid-covid-data.json ##

echo -ne "Fitting curves...               \r" ##
python3 curve_fitting.py > results.json ##
echo -ne '#########...................(33%)\r'

echo "Ploting curves...                      " ##
python3 plot_curves.py ##
echo -ne '##################..........(66%)\r'

cd .. ##
cd Covid-19-Country-Graphs/ ##

echo "Pushing changes to Github...             \r" ##
git stage * ##
now=$(date +'%m/%d/%Y') ##
git commit -m "$now" ##
git push ##
echo -ne '###########################(100%)\n'