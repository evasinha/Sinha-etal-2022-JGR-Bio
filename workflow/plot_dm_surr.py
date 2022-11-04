import os
import numpy as np
import pickle as pk

import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
from optparse import OptionParser

from plotutils import *

parser = OptionParser();

parser.add_option("--site", dest="site", default="", \
                  help="Site ID")
parser.add_option("--crop", dest="crop", default="", \
                  help="Modeled crop name")

(options, args) = parser.parse_args()

#----------------------------------------------------------
# plot_mod_dm is modified from plot_dm provided by Khachik Sargsyan
def plot_mod_dm(datas, models, showlabel=False, xlabel=None, ax=None, labels=[],
            legendpos='in', msize=4):
    """Plots data-vs-model and overlays y=x"""

    ncase = len(datas)
    if labels == []:
        labels = [''] * ncase

    # Create colors list
    colors = set_colors(ncase)
    yy = np.empty((0, 1))
    for i in range(ncase):
        data = datas[i]
        model = models[i]
        npts = data.shape[0]
        neach = 1
        if (data.ndim > 1):
            neach = data.shape[1]

        ddata = data.reshape(npts, neach)

        for j in range(neach):
            yy = np.append(yy, ddata[:, j])
            ax.plot(ddata[:, j], model, 'o', color=colors[i], label=labels[i], markersize=msize)

    delt = 0.1 * (yy.max() - yy.min())
    minmax = [yy.min() - delt, yy.max() + delt]
    ax.plot(minmax, minmax, 'r', linewidth=1.5, label='y=x')

    # Add x axis label
    ax.set_xlabel(xlabel)
    
    # Turn off grid
    ax.grid(False)

    if showlabel:
        if legendpos == 'in':
            ax.legend()
        elif legendpos == 'out':
            ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5),
                      ncol=1, fancybox=True, shadow=True)

    # Trying to make sure both axis have the same number of ticks
    ax.xaxis.set_major_locator(plt.MaxNLocator(7))
    ax.yaxis.set_major_locator(plt.MaxNLocator(7))

    return ax
#----------------------------------------------------------

myrc()

# ---------------------------------------------------------
# open the results stored as a pickled file
os.chdir('../site_calib_outputs/')

results = pk.load(open(options.site + '_' + options.crop + '_' + 'results_all.pk', 'rb'))

# Dictionary for day of year and corresponding day
myDict = {'GPP': {'152':'June 1',  '182':'July 1',  '213':'Aug 1',  '244':'Sept 1',  '274':'Oct 1'},
          'ER':  {'517':'June 1',  '547':'July 1',  '578':'Aug 1',  '609':'Sept 1',  '639':'Oct 1'},
          'LE':  {'882':'June 1',  '912':'July 1',  '943':'Aug 1',  '974':'Sept 1',  '1004':'Oct 1'},
          'H':   {'1247':'June 1', '1277':'July 1', '1308':'Aug 1', '1339':'Sept 1', '1369':'Oct 1'}}

#iterate through dictionary
for i, key1 in enumerate(myDict):

    fig, ax = plt.subplots(nrows=1, ncols=len(myDict[key1]), sharex=True, sharey=True, figsize=(25, 5), constrained_layout=True)

    for j, key2 in enumerate(myDict[key1]):
        
        index = int(key2)
            
        ntrn = int(0.9 * results[index]['ycheck'].shape[0])

        if (key1 == 'H' and j == 0):
            showlabel = True
        else:
            showlabel = False

        if (key1 == 'H'):
            xlabel = 'Sim. of ELM (' + myDict[key1][key2] + ')'
        else:
            xlabel = None
        
        plot_mod_dm([results[index]['yall'][:ntrn], results[index]['yall'][ntrn:]],
                    [results[index]['ycheck'][:ntrn], results[index]['ycheck'][ntrn:]],
                    showlabel, xlabel,
                    ax=ax[j],
                    labels=['Training', 'Testing'])

    if (key1 == 'GPP'):
        ax[0].text(0.02, 0.93, options.crop, color='black', transform=ax[0].transAxes, fontsize=18, bbox=dict(facecolor='white', edgecolor='white'))
        ax[0].text(0.80, 0.93, options.site,  color='black', transform=ax[0].transAxes, fontsize=18, bbox=dict(facecolor='white', edgecolor='white'))

    ax[0].set_ylabel('Sim. of surrogate')
    ax[4].text(0.80, 0.93, key1,   color='black', transform=ax[4].transAxes, fontsize=20, bbox=dict(facecolor='white', edgecolor='white'))

    plt.savefig('../figures/' + 'fit_' + options.site + '_' + options.crop +'_' + key1 + '.png', bbox_inches='tight')
