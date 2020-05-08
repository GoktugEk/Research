import os
import time

t1 = time.time()


os.system("python3 curve_fitting.py > results.json")
os.system("python3 plot_curves.py")
os.system("cd Graphs")
os.system("git init")
os.system("git add .")
os.system('git commit -m "May 8"')
os.system("git remote rm origin")
os.system('git remote add origin git@github.com:teghub/Covid-19-Country-Graphs.git')
os.system("git push -f origin master")
t2 = time.time()
seconds = t2-t1
minutes = seconds//60
seconds = seconds - minutes*60
print("Execute time is {}:{}".format(minutes,seconds))