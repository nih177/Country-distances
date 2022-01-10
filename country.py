# ***************************************************************************
# Please read comments for better understanding of code and how to customize
# ***************************************************************************
from matplotlib.pyplot import waitforbuttonpress
import click
import requests
import json
from datetime import datetime
from math import radians, cos, sin, asin, sqrt, pi

headers = { "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0"}

# This is the function that calculates the distance between places using latitudes and longitudes
def distances(lat1, lon1, lat2, lon2):
    p = pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 12742 * asin(sqrt(a))

def myFunc(e):
  return e['population']

# This is the main function
def mainfun(population_limit,utmosts):
    # Getting the data from the URL
    api_url = "https://cdn.jsdelivr.net/gh/apilayer/restcountries@3dc0fb110cd97bce9ddf27b3e8e1f7fbe115dc3c/src/main/resources/countriesV2.json"
    req = requests.get(url=api_url, headers=headers)
    data = req.json()
    total_coutries = len(data)
    total_sum = 0
    # Creating a list with length utmost no.
    new_lis = [] * utmosts
    exculsive_cur = 1
    # This loop will filter the countries
    for k in range(0,total_coutries-1):
        if data[k]['population'] >= population_limit:
            for x in range(0,len(data[k]['currencies'])):
                for l in range(0,total_coutries):
                    if k != l:
                        for y in range(0,len(data[l]['currencies'])):
                            if data[k]['currencies'][x]['code'] == data[l]['currencies'][y]['code']:
                                exculsive_cur = 0
                                break
                if exculsive_cur == 1:
                    new_lis.append(data[k])
                exculsive_cur = 1
    print('This is the no. of countries that satistfy the given criteria')
    print(len(new_lis))
    print('\n')
    # Sorting the new list (Since in my question they asked to sort)
    new_lis.sort(key=myFunc)
    for i in range(0,utmosts):
        for j in range(i+1,utmosts):
            if len(new_lis[i]['latlng']) == 0:
                new_lis[i]['latlng'].append(0.000)
                new_lis[i]['latlng'].append(0.000)
            if len(new_lis[j]['latlng']) == 0:
                new_lis[j]['latlng'].append(0.000)
                new_lis[j]['latlng'].append(0.000)
            distance_between = distances(new_lis[i]['latlng'][0],new_lis[i]['latlng'][1],new_lis[j]['latlng'][0],new_lis[j]['latlng'][1])
            # Here we are rounding the each line's lenght to two decimals
            rou = round(distance_between, 2)
            total_sum += rou
            # Here we are rounding the total lenght to two decimals
            total_sum = round(total_sum,2)
    # This is the final result rounded to two decimals (In my question I have to round to 2 decimals change according to your condition)
    print('**********************')
    print('Total sum = ',total_sum)
    print('**********************')
print('Please enter the population limit')
population_limits = int(input())
print('Enter the utmost no. of countries (In my question its 20.Enter what they are asking in your question)')
utmost = int(input())
mainfun(population_limits,utmost)
