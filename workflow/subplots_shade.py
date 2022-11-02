#!/usr/bin/env python

import os
import argparse
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
from scipy.stats.mstats import mquantiles
import scipy.stats

#----------------------------------------------------------

plt.rc('legend', loc='best', fontsize=18)
plt.rc('lines', linewidth=4, color='r')
plt.rc('axes', linewidth=1, grid=True, labelsize=18)
plt.rc('xtick', labelsize=18)
plt.rc('ytick', labelsize=18)

# ---------- function for estimating root mean square error ----------
def rmse(model, obs):
    return np.sqrt(((model - obs) ** 2).mean())

# ---------- function for estimating bias ----------
def bias(model, obs):
    return (model - obs).mean()

# ---------- function for estimating percent absolute bias ----------
def per_abs_bias(model, obs):
    return 100 * sum((abs(model - obs)))/sum(obs)

# ---------- function for estimating percent bias ----------
def per_bias(model, obs):
    return 100 * sum((model - obs))/sum(obs)

##########################################################################


def plot_shade(ax, xdata, ydata, nq=51, cmap=mpl.cm.BuGn,
               bounds_show=False, grid_show=True):
    nx = xdata.shape[0]
    assert(nx == ydata.shape[0])

    mq = mquantiles(ydata, prob=[float(i + 1) / float(nq)
                                 for i in range(nq - 1)], axis=1)
    #ax.sca(ax)

    normalize = mpl.colors.Normalize(vmin=0.01, vmax=0.5)

    for k in range(int(nq / 2)):
        ax.fill_between(xdata, mq[:, k], mq[:, k + 1],
                         color=cmap(normalize(0.01 + k * .02)))
    for k in range(int(nq / 2), nq - 2):
        ax.fill_between(xdata, mq[:, k], mq[:, k + 1],
                         color=cmap(normalize(0.5 - (k - nq / 2) * 0.02)))
    if bounds_show:
        ax.plot(xdata, mq[:, 0], linewidth=2, color="grey")
        ax.plot(xdata, mq[:, -1], linewidth=2, color="grey")

    ax.set_xlim([0,365])
    # Define the month format
    #ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    #ax.xaxis.set_major_formatter(DateFormatter('%d-%b'))
    
    ax.grid(grid_show)

    return ax
##########################################################################

# custom_xlabel = ''
# custom_ylabel = ''
# custom_ylim = [-1, 10]
# custom_title = args.title

# Parse input arguments
usage_str = 'Script to plot shaded PDF fits to a given slice of outputs.'
parser = argparse.ArgumentParser(description=usage_str)
parser.add_argument("-site", "--site", dest="site",
                    type=str, default='', help="Site ID")
parser.add_argument("-crop", "--crop", dest="crop",
                    type=str, default='', help="Modeled crop name")
parser.add_argument("-k", "--ind_y_stat", dest="ind_y_stat_file", type=str,
                    default=None, help="File for indices to use for summary statistics")
parser.add_argument("-x", "--xdata", dest="xdata_file",
                    type=str, default=None, help="Xdata file")
parser.add_argument("-y", "--prior_out", dest="prior_output_file",
                    type=str, default=None, help="Prior output file")
parser.add_argument("-z", "--post_out", dest="post_output_file",
                    type=str, default=None, help="Posterior output file")
parser.add_argument("-s", "--ydata_std", dest="datastd_file",
                    type=str, default=None, help="Data st. deviation file")
parser.add_argument("-c", "--ncol", dest="ncol",
                    type=int, default=1, help="The relevant column of xdata file (count from 0)")
parser.add_argument("-u", "--xlabel", dest="xlabel",
                    type=str, default='', help="X label")
parser.add_argument("-l", "--xticklabels", dest="xticklabels_file",
                    type=str, default=None, help="Xtick labels file")
parser.add_argument("-ylb", "--ylim_bot", dest="ylim_bot",
                    type=float, default=None, help="yaxis bottom limit")

args = parser.parse_args()

site = args.site
crop = args.crop
ind_y_stat_file = args.ind_y_stat_file
prior_output_file = args.prior_output_file
post_output_file = args.post_output_file
datastd_file = args.datastd_file
xdata_file = args.xdata_file
ncol = args.ncol
custom_xlabel = args.xlabel
ylim_bot = args.ylim_bot

os.chdir('../site_calib_outputs/')

if args.xticklabels_file is not None:
    with open(args.xticklabels_file) as f:
        custom_xticklabels = f.read().splitlines()

    #custom_xticklabels = np.loadtxt(args.xticklabels, dtype=str) # ideally read

prior_out_flag = False
if prior_output_file is not None:
    prior_output = np.loadtxt(prior_output_file)
    prior_out_flag = True
    nout = prior_output.shape[1]

post_out_flag = False
if post_output_file is not None:
    post_output = np.loadtxt(post_output_file)
    post_out_flag = True
    nout = post_output.shape[1]

assert(prior_out_flag or post_out_flag)
assert(prior_output.shape[1] == post_output.shape[1])

myDict = {'GPP': 'GPP [$\mathregular{gC~m^{-2}~day^{-1}}$]',
          'ER':  'ER [$\mathregular{gC~m^{-2}~day^{-1}}$]',
          'LE':  'LE [$\mathregular{W~m^{-2}}$]',
          'H':   'H [$\mathregular{W~m^{-2}}$]'}

fig, ax = plt.subplots(nrows=len(myDict), ncols=1, sharex=True, sharey=False, figsize=(8, 5*len(myDict)), constrained_layout=True)

for i, key in enumerate(myDict):

    indplot_file    = site + '_' + crop + '_' + 'ind_plot_' + key + '.dat'
    data_file       = site + '_' + crop + '_' + 'ydata_plot_' + key + '.dat'
    ind_y_stat_file = site + '_' + crop + '_' + 'ind_y_stat_' + key + '.dat'
    ind_z_stat_file = site + '_' + crop + '_' + 'ind_z_stat_' + key + '.dat'

    if indplot_file is not None:
        ind_plot = np.loadtxt(indplot_file, dtype=int)
    else:
        ind_plot = np.arange(nout)

    if ind_y_stat_file is not None:
        ind_y_stat = np.loadtxt(ind_y_stat_file, dtype=int)
    else:
        ind_y_stat = np.arange(nout)

    if ind_z_stat_file is not None:
        ind_z_stat = np.loadtxt(ind_z_stat_file, dtype=int)
    else:
        ind_z_stat = np.arange(nout)

    if xdata_file is not None:
        xdata = np.loadtxt(xdata_file)[ind_plot, ncol]
    else:
        xdata = np.arange(nout)

    nout_plot = ind_plot.shape[0]

    thisax = ax[i]

    if prior_out_flag:
        plot_shade(thisax, xdata,
                  prior_output[:, ind_plot].T, cmap=cm.OrRd, grid_show=True)
    if post_out_flag:
        plot_shade(thisax, xdata,
                  post_output[:, ind_plot].T, nq=21, grid_show=True)


    #thisax.set_xticks(xdata)

    if data_file is not None:
        bcg_data = np.loadtxt(data_file, ndmin=2)
        for j in range(bcg_data.shape[1]):
            if datastd_file is not None:
                bcg_data_std = np.loadtxt(datastd_file, ndmin=2)
                thisax.errorbar(xdata, bcg_data[:, j], yerr=bcg_data_std[:, j],
                                ecolor='k', fmt='ko', label='Data', ms=12, zorder=100000)
            else:
                thisax.plot(xdata, bcg_data[:, j], 'k', label='Data', linewidth=2.0, zorder=100000)

    try:
        thisax.set_xticklabels(custom_xticklabels)
    except NameError:
        pass

    if ylim_bot is not None:
        thisax.set_ylim(bottom = ylim_bot)
    try:
        thisax.set_ylim(custom_ylim)
    except NameError:
        pass

    thisax.set_xlabel(custom_xlabel)
    thisax.set_ylabel(myDict[key])
    #thisax.set_title(custom_title, size=24)

    handles, labels = thisax.get_legend_handles_labels()
    handles.append(plt.Rectangle((0, 0), 1, 1, fc='r'))
    labels.append('Prior')
    handles.append(plt.Rectangle((0, 0), 1, 1, fc='g'))
    labels.append('Posterior')
    thisax.grid(False)

    output = open(site + '_' + crop + '_' + 'summary_stats_' + key + '.txt','w')
    output.write(crop + ' - Summary stats for the calibration window ' + '\n')
    output.write('RMSE ' + str(rmse(post_output[:, ind_z_stat].mean(axis=0), bcg_data[ind_y_stat].squeeze())) + '\n')
    output.write('Bias ' + str(bias(post_output[:, ind_z_stat].mean(axis=0), bcg_data[ind_y_stat].squeeze())) + '\n')
    output.write('Percent bias ' + str(per_bias(post_output[:, ind_z_stat].mean(axis=0), bcg_data[ind_y_stat].squeeze())) + '\n')
    output.write('R2 ' + str(scipy.stats.linregress(bcg_data[ind_y_stat].squeeze(), post_output[:, ind_z_stat].mean(axis=0)).rvalue) + '\n')
    output.write('pvalue ' + str(scipy.stats.linregress(bcg_data[ind_y_stat].squeeze(), post_output[:, ind_z_stat].mean(axis=0)).pvalue) + '\n')
    output.write(crop + ' - Summary stats for all days in the year' + '\n')
    output.write('RMSE ' + str(rmse(post_output[:, ind_plot].mean(axis=0), bcg_data.squeeze())) + '\n')
    output.write('Bias ' + str(bias(post_output[:, ind_plot].mean(axis=0), bcg_data.squeeze())) + '\n')
    output.write('Percent bias ' + str(per_bias(post_output[:, ind_plot].mean(axis=0), bcg_data.squeeze())) + '\n')
    output.write('R2 ' + str(scipy.stats.linregress(bcg_data.squeeze(), post_output[:, ind_plot].mean(axis=0)).rvalue) + '\n')
    output.write('pvalue ' + str(scipy.stats.linregress(bcg_data.squeeze(), post_output[:, ind_plot].mean(axis=0)).pvalue) + '\n')
    output.close()

ax[len(myDict)-1].legend(handles, labels, fontsize=18, ncol=1)
ax[0].text(0.02, 0.93, crop, color='black', transform=ax[0].transAxes, fontsize=18, bbox=dict(facecolor='white', edgecolor='white'))
ax[0].text(0.82, 0.93, site,  color='black', transform=ax[0].transAxes, fontsize=18, bbox=dict(facecolor='white', edgecolor='white'))

# Define the month format
ax[len(myDict)-1].xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax[len(myDict)-1].xaxis.set_major_formatter(DateFormatter('%d-%b'))

plt.savefig('../figures/' + site + '_' + crop + '_' + 'fit_shade.png', bbox_inches='tight')
# show()
