#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 22:00:45 2016

Reads a list of events by date and plots a moving average and day of the week
histogram.

Modules:
eventdates.py -- a file where the events are documented; contains 2 variables:
    event1 -- event series 1
    event2 -- event series 2
    
    Each variable is a list of dates with format (YYYY, MM, DD, HH)
    e.g.
        event1 = [
        (2016, 10, 24, 12),
        (2016, 09, 15, 12),
        (2016, 08, 31, 12),
        ]

@author: arcosdid
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_palette('Paired')
sns.set_style("whitegrid")

from eventdates import *

#%% READ DATA AND CALCULATE MOVING AVERAGE

# Read the event series 1
df1 = pd.DataFrame(event1)
df1 = pd.to_datetime(df1[0]*10000 + df1[1]*100 + df1[2], format='%Y%m%d')
df1 = pd.DataFrame(df1)
df1['Event1'] = pd.Series(np.ones(len(df1)+10))
df1.columns=(['Date', 'Event1'])

# Read the event series 2
df2 = pd.DataFrame(event2)
df2 = pd.to_datetime(df2[0]*10000 + df2[1]*100 + df2[2], format='%Y%m%d')
df2 = pd.DataFrame(df2)
df2['Event2'] = pd.Series(np.ones(len(df2)+10))
df2.columns=(['Date', 'Event2'])

# Concatenate both dataframes into one
df = pd.concat([df1, df2], ignore_index=True)
df = df.set_index('Date')
df = df.sort_index()
df = df.resample('1d').sum().fillna(0) # to complete every day

# Calculate moving average
for i in [7*4, 7*4*2]:
    mvav = i # moving average period, i.e. number of points to average
    dfi = np.convolve(df['Event1'], 
                      np.ones((mvav,))*7/mvav # factor for obtaining average
                      , mode='full')
    df['Event1 Moving average %sw' % (int(i/7))] = dfi[:-(i-1)]
    dfj = np.convolve(df['Event2'], 
                      np.ones((mvav,))*7/mvav # factor for obtaining average
                      , mode='full')
    df['Event2 Moving average %sw' % (int(i/7))] = dfj[:-(i-1)]

# Plot relevant columns from dataframe
df.loc[:,['Event1', 'Event2 Moving average 8w', 'Event1 Moving average 8w']].\
plot(cmap='Blues') #figsize=(8,4) possible
plt.xlim(df.index[0], df.index.max()+10)
plt.title('Moving average of events per week')
plt.show()

#%% DAY OF THE WEEK ANALYSIS

# create column for day of the week
df['Day'] = df.index.dayofweek
df['Day'] = df.Day.astype('category')
df.Day.cat.categories = ['Mon','Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

# create column for type
df['Type'] = np.where(df['Event1']>0, 'event1', np.where(df['Event2']>0,\
 'event2', np.nan))
df['Type'] = df['Type'].astype('category')
df['Type'] = df['Type'].cat.remove_categories(['nan'])

# show count for each day
#df[(df.Event1 == 1)&(df.Day == 'Mon')].Day.count()

# plot count data per day of the week
plt.figure()
plt.title('Event count per day of the week')
sns.countplot(data=df, x='Day', hue='Type')
sns.despine(left=True)
plt.show()

# joint histograms
plt.figure()
df['Event2 Moving average 8w'].hist(alpha=.9)
df['Event1 Moving average 8w'].hist(alpha=.9)
plt.title('Histogram of event frequency per week')
plt.show()

#%% histograms side-by-side
df.loc[:,['Event2 Moving average 8w', 'Event1 Moving average 8w']].hist()
plt.show()

# With seaborn
sns.distplot(df['Event1 Moving average 8w']), \
sns.distplot(df['Event2 Moving average 8w'])
