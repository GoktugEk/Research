import os
import time
from datetime import date



commit_date = str(date.today())



commit = 'git commit -m "' + commit_date + '"'

t1 = time.time()


os.system("python3 curve_fitting.py > results.json")
os.system("python3 plot_curves.py")

os.chdir("/home/goktu/Desktop/Covid-19-Country-Graphs/")
os.system("git stage *")
os.system(commit)
os.system("git push")
t2 = time.time()
seconds = t2-t1
minutes = int(seconds//60)
seconds = int(seconds - minutes*60)
print("Execute time is {}:{}".format(minutes,seconds))
