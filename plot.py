__author__ = 'marco'
__license__ = "MIT"

import pandas as pd
import numpy as np
from datetime import datetime
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns


# Import the dataset
parse = lambda x: datetime.datetime.fromtimestamp(float(x)/1000)
sliceSum = pd.read_csv('datasets/sms-call-internet-tn-2013-11-01.txt', delim_whitespace=True, names=['GridCell', 'datetime','countryCode', 'callin', 'callout', 'smsin', 'smsout' ,'internet'], encoding="utf-8-sig", parse_dates=['datetime'], date_parser=parse)

# Set the index as timestamp
sliceSum = sliceSum.set_index(['datetime'], drop=False)
sliceSum.index = sliceSum.index.tz_localize('UTC').tz_convert('Europe/Rome')

# Group everything, ignoring the countrycode and the days
sliceSum = sliceSum.groupby(['GridCell'], as_index=False).sum()
del sliceSum['countryCode']

# Absolute
sliceSum['day'] = sliceSum.index.weekday
abs_df = sliceSum.groupby(['day', sliceSum.index.hour]).mean()

# Z-scale
weekly_df = sliceSum
weekly_df = weekly_df.groupby(['day', sliceSum.index.hour]).mean()
weekly_df = (weekly_df - weekly_df.mean()) / weekly_df.std()

# Style managment
sns.set_palette(sns.color_palette("Blues_r"))
sns.set_style("white")

types = ['smsin', 'smsout', 'callsin', 'callsout', 'internet']

# Plot of mean absolute values
lines = []
f, axs = plt.subplots(len(types), sharex=True, sharey=True,figsize=(8,11))
for i,p in enumerate(types):

    plt.xticks(np.arange(168, step=8))
    axs[i].plot(abs_df[p], label=p)
    axs[i].legend()
    sns.despine()

f.text(0.075, 0.5, "Number of events", rotation="vertical", va="center")

plt.xlabel("Hour (in a week)")
plt.savefig('absbehaviour.pdf', format='pdf', dpi=330,bbox_inches='tight')

# Plot of mean Z-scaled values
lines = []
f, axs = plt.subplots(len(types), sharex=True, sharey=True,figsize=(8,11))
for i,p in enumerate(types):

    plt.xticks(np.arange(168, step=8))
    axs[i].plot(weekly_df[p], label=p)
    axs[i].legend()
    sns.despine()

f.text(0.075, 0.5, "Number of events", rotation="vertical", va="center")

plt.xlabel("Hour (in a week)")
plt.savefig('behaviour.pdf', format='pdf', dpi=330,bbox_inches='tight')

#
# Boxplots
#
we_df = sliceSum.groupby(['day','gridcell']).mean()
types_lim = [70, 70, 60, 60, 900]

for i,p in enumerate(types):
    ax = we_df.reset_index().boxplot(column=p,by='day', grid=False)
    ax.set_ylim([0, types_lim[i]])
    plt.title("Average number of "+p+" events per day and grid square")
    plt.suptitle("")
    plt.ylabel("Number of events")
    plt.xlabel("Weekday (0=Monday, 6=Sunday)")
    sns.despine()
    plt.savefig('boxplot-'+p+'.pdf', format='pdf', dpi=330,bbox_inches='tight')
