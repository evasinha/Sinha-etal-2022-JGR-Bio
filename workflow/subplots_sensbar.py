#!/usr/bin/env python

import os
import numpy as np
import pandas as pd
import seaborn as sns
import pickle as pk
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
from optparse import OptionParser


import utils as mu

parser = OptionParser();

parser.add_option("--site", dest="site", default="", \
                  help="Site ID")
parser.add_option("--crop", dest="crop", default="", \
                  help="Modeled crop name")

(options, args) = parser.parse_args()

#----------------------------------------------------------

############################################################
############################################################
############################################################
# should be run after elm_fates/run_wibcs.py
############################################################
############################################################
############################################################

plt.rc('figure', titlesize=15)
plt.rc('legend', fontsize=15, title_fontsize=15)
plt.rc('axes',   labelsize=15, titlesize=15)
plt.rc('xtick',  labelsize=15)
plt.rc('ytick',  labelsize=15)

# ---------------------------------------------------------
os.chdir('../site_calib_outputs/')

results_all = pk.load(open(options.site + '_' + options.crop + '_' + 'results_all.pk', 'rb'))

nout = len(results_all)
dim = 12

myDict = {'GPP': 365, 'ER': 730, 'LE': 1095, 'H': 1460}

for ind, key in enumerate(myDict):

    ind_plot=np.arange(myDict[key]-365,myDict[key]) # change this to (0,365) for one variable, (365, 730) for two variables, and (730, 1095) when 3 variables

    pars = range(dim)
    nout_plot = len(ind_plot)
    cases = np.arange(nout_plot)

    pnames = mu.read_textlist('pnames.txt', dim)
    outnames = [str(j+1) for j in range(nout_plot)]

    all_totsens = np.zeros((nout_plot, dim))
    all_mainsens = np.zeros((nout_plot, dim))
    for i in range(nout_plot):
        iout = ind_plot[i]
        print("================================================================")
        print("Output %d / %d" % (iout + 1, nout))
        print("================================================================")
        if results_all[iout] is not None:
            #print(results_all[iout].keys())
            mindex = results_all[iout]['mindex']
            pccf = results_all[iout]['cfs']
            a, b = mu.encode_mindex(mindex)
            # for i, j in zip(a, b):
            #     print(i, j)

            mainsens, totsens, jointsens, mean, var = mu.pce_sens('LU',
                                                                  mindex,
                                                                  pccf,
                                                                  mv=True)

            all_totsens[i, :] = totsens
            all_mainsens[i, :] = mainsens

    #colors = ut.set_colors(22)
    cmap = plt.get_cmap('tab20')
    colors = np.array([cmap(j) for j in np.arange(dim)/(dim-1)])

    if (ind == len(myDict)-1):
        xtick_labels = True
    else:
        xtick_labels = False

    df = pd.DataFrame(all_mainsens, columns=pnames)
    df = pd.melt(df, var_name='pnames')
    df['QoI'] = key

    if(ind == 0):
       df_plot = df
    else:
       # Combine into in a single dataframe
       df_plot = pd.concat([df_plot, df], axis=0)

# make bar plot
g = sns.catplot(data=df_plot, x='pnames', y='value', row='QoI',  kind='bar', palette=colors, height=3, aspect=2)
#g = sns.catplot(data=df_plot, x='pnames', y='value', row='QoI',  kind='bar', errorbar='sd',  palette=colors, height=3, aspect=2)

# Rotate xtick labels
g.set_xticklabels(labels=pnames, rotation=90)

# Modify axis labels
for i, ax in enumerate(g.axes.flat):
   if ax.get_title():
      ax.set_ylabel(ax.get_title().split('=')[1] + ' - Sensitivity')

      if(i == 0):
         ax.text(0.02, 0.93, options.crop, color='black', fontsize=15, transform=ax.transAxes)
         ax.text(0.85, 0.93, options.site, color='black', fontsize=15, transform=ax.transAxes)

   ax.set_xlabel('') # remove x axis label

# Remove facet titles
g.set_titles(row_template='')

plt.savefig('../figures/' + options.site + '_' + options.crop + '_' + 'sensbar_main_all.png', bbox_inches='tight')
