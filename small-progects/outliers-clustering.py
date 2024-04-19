#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 12:28:09 2023

@author: saraveradi

File to solve python mini task
The task is to use box plot to omit outliers
I want to use a simple and fast solution which I write
It is not interactive, so I use the concept to
creat my own solution
"""

# =============================================================================
# Importing libraries
# =============================================================================
import numpy  as np
import pandas as pd
import matplotlib.pyplot as plt
from   sklearn.cluster   import KMeans 
#%% ===========================================================================
# Importing clean data
# =============================================================================
df = pd.read_excel(r'/home/saraveradi/Documents/dataset1.xlsx')

#%% ===========================================================================
# Visualizing Box plots
# =============================================================================

# df.boxplot(column = 'distance');
# df.boxplot(column = 'time');

#%% ===========================================================================
# Using Box-plot methodology to omit outliers
# =============================================================================
data = df.to_numpy()                      #preserving our data

# Computing boxs' margins
p25, p50, p75 = np.percentile([df.distance, df.time], [25, 50, 75], axis=1)
print(p25, p50, p75)

IQR = p75 - p25                           #Interquartile range
print('Interquartile range is', IQR)

# Change the numbers bellow to decide which data you want to omit
low_lim = p25 - 1.5 * IQR                 # the lowest limits 
up_lim  = p75 + 4 * IQR                 # the highest limits

print('low_limit is', low_lim)            # first element is distance
print('up_limit is', up_lim)

#%%============================================================================
# Ommitting outliers of distance and related data of time 
# =============================================================================
distance = data[:,0]
time     = data[:,1]

index    = (distance > low_lim[0])

distance = distance[index]
time     =     time[index]

index    = (distance < up_lim[0])

distance = distance[index]
time     =     time[index]


# =============================================================================
# Ommitting outliers of time and related data of distance
# =============================================================================
index    = (time > low_lim[1])

time     = time[index]
distance = distance[index]

index    = (time <  up_lim[1])

time     = time[index]
distance = distance[index]

#%%
# Visualize data points

plt.scatter(distance, time)
plt.xlabel('distance')
plt.ylabel('time')
plt.show()

#%% ===========================================================================
# Clusteringd : Elbow
# =============================================================================

dataclean = np.column_stack( (distance, time))   #Suitable data format for kmeans

inertias = []

# Trying to decide on the number of clusters

for i in range(1,11):
    kmeans = KMeans(n_clusters=i)
    kmeans.fit(dataclean)
    inertias.append(kmeans.inertia_)

plt.plot(range(1,11), inertias, marker='o')
plt.title('Elbow method')
plt.xlabel('Number of clusters')
plt.ylabel('Inertia')
plt.show() 

#%% ===========================================================================
# Decide number of clusters based on the Elbow Method above
# =============================================================================

kmeans = KMeans(n_clusters=2)
kmeans.fit(dataclean)

plt.scatter(distance, time, c=kmeans.labels_, alpha=0.7)
plt.show() 