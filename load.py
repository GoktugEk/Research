import urllib.request

print("Downloading the data...",end = '\r')
url = "https://covid.ourworldindata.org/data/owid-covid-data.json"
urllib.request.urlretrieve(url, '/home/goktu/Desktop/Research/owid-covid-data.json')