import os
import time
import urllib.request
from datetime import date

t1 = time.time()

commit_date = str(date.today())
commit = 'git commit -m "' + commit_date + '"'

print("Downloading the data...")

url = "https://covid.ourworldindata.org/data/owid-covid-data.json"
urllib.request.urlretrieve(url, '/home/goktu/Desktop/Research/owid-covid-data.json')


print("Fitting curves and getting parameters...")
os.system("python3 curve_fitting.py > results.json")

print("Plotting curves...")
os.system("python3 plot_curves.py")

print("Pushing changes to Github...")
os.chdir("/home/goktu/Desktop/Covid-19-Country-Graphs/")
os.system("git stage *")
os.system(commit)
os.system("git push")

t2 = time.time()

seconds = t2-t1
minutes = int(seconds//60)
seconds = int(seconds - minutes*60)

print("Execute time is {}:{}".format(minutes,seconds))
