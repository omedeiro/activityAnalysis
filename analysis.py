# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 10:48:46 2021

@author: omedeiro
"""

import xmltodict
from matplotlib import pyplot as plt
import numpy as np
import datetime
from collections import Counter
from collections import defaultdict
import ipyhealth
import os
from dateutil.relativedelta import *


abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
    
# input_path = r'G:\My Drive\personal\health\data\20210428\apple_health_export\export.xml'
input_path = 'export.xml'
with open(input_path, 'r') as xml_file:
    input_data = xmltodict.parse(xml_file.read())
    

#%%
workouts_list = input_data['HealthData']['Workout']


running_data = np.array([0,0,0])
for workouts in workouts_list:
    if workouts['@workoutActivityType'] == 'HKWorkoutActivityTypeRunning':
        date = workouts['@startDate'][0:19]
        date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        duration = float(workouts['@duration'])
        distance = float(workouts['@totalDistance'])
        line = np.array([date.timestamp(), duration, distance])
        running_data = np.vstack([running_data, line])

running_data = np.delete(running_data, 0, 0)


dates = [datetime.datetime.fromtimestamp(x).date() for x in running_data[:,0]]

'''
 Fix workouts where I hit "stop" instead of "pause". 
Then add the two workouts on the same day together
'''
D = defaultdict(list)
for i,item in enumerate(dates):
    D[item].append(i)
D = {k:v for k,v in D.items() if len(v)>1}

del_rows=[]
tot_rows = np.array([0,0,0])
for d in list(D.values()):
    total_dis = np.sum(running_data[d, 2])
    total_time = np.sum(running_data[d, 1])
    del_rows.extend(d)
    
    new_row = np.array([running_data[d[0],0], total_time, total_dis])
    tot_rows = np.vstack([tot_rows, new_row])

tot_rows = np.delete(tot_rows, 0, 0)
runningTotal = np.delete(running_data, del_rows, 0)
runningTotal = np.vstack([runningTotal, tot_rows])

runningTotal = runningTotal[np.argsort(runningTotal[:, 0])]
dates = [datetime.datetime.fromtimestamp(x).date() for x in runningTotal[:,0]]

plt.figure()
plt.plot(dates, runningTotal[:,2], '-o')
plt.gcf().autofmt_xdate()
plt.ylabel('distance (mi)')

plt.figure()
plt.plot(dates, runningTotal[:,1], '-o')
plt.gcf().autofmt_xdate()
plt.ylabel('duration (min)')

print("LONGEST RUN      : %0.2f mi" %(max(runningTotal[:,2])))
print("TOTAL MILES      : %0.2f mi" %(sum(runningTotal[:,2])))

#%% 
monthyear = []
for d in dates:
    yindex = d.year-2019
    mont = d.month
    monthyear.append((12*yindex+mont)-1)
plt.close()        
bins=np.arange(0, max(monthyear)+1+yindex)
fig, ax = plt.subplots(1,1, figsize=(10, 3), facecolor='white')
ax.hist(monthyear, bins=bins, ec='black') #good
ax.set_xticks(bins[:-2]+0.5) #good
ax.set_xticklabels([(datetime.date(2019, 1, 1)+relativedelta(months=i)).strftime('%b %Y') for i in bins[:-1]], rotation=90)

plt.ylabel('Runs')

