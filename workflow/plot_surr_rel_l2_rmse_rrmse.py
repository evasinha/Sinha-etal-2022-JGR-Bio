import os
import matplotlib as mpl
mpl.use('Agg')
import numpy as np
import pickle as pk

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
from optparse import OptionParser

parser = OptionParser();

parser.add_option("--site", dest="site", default="", \
                  help="Site ID")
parser.add_option("--crop", dest="crop", default="", \
                  help="Modeled crop name")

(options, args) = parser.parse_args()

#----------------------------------------------------------
def myrc():
    # Plot model and observations
    parameters = {'figure.titlesize':18,
                  'legend.fontsize': 18,
                  'axes.labelsize' : 18,
                  'axes.titlesize' : 18,
                  'xtick.labelsize': 18,
                  'ytick.labelsize': 18,
                  'font.size'      : 18}
    
    plt.rcParams.update(parameters)

#----------------------------------------------------------
def plot_timeseries(ds_plot, site, title, varname, ylabel, metric):
    """Plot timeseries from input xarray
    :param: ds_plot        2d numpy array to plot
    :param: title:         variable title for plotting
    :param: varname:       variable name
    :param: ylabel:        variable ylabel for plotting
    """
        
    fig, ax = plt.subplots(figsize=(11, 8.5))
    plt.plot(ds_plot[:,0], ds_plot[:,1], color='black')
    plt.ylabel(ylabel)
    plt.yscale('log')
    plt.text(0.01, 1.05, title,   color='black', transform=ax.transAxes, fontsize=18, bbox=dict(facecolor='white', edgecolor='white'))
    plt.text(0.90, 1.05, varname, color='black', transform=ax.transAxes, fontsize=18, bbox=dict(facecolor='white', edgecolor='white'))
 
    # Define the month format
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    plt.gca().xaxis.set_major_formatter(DateFormatter('%d-%b'))
            
    plt.savefig('../figures/'+ site + '_'  + title + '_' +  varname + '_' + metric + '.png', bbox_inches='tight') 

#----------------------------------------------------------
def plot_timeseries_subplots(ds_plot, site, title, ylabel, metric):
    """Plot timeseries from input xarray
    :param: ds_plot        2d numpy array to plot
    :param: title:         variable title for plotting
    :param: ylabel:        variable ylabel for plotting
    """

    myDict = {'GPP': 365, 'ER': 730, 'LE': 1095, 'H': 1460}
    myDict_label = {'GPP': 'RMSE [$\mathregular{gC~m^{-2}~day^{-1}}$]',
                    'ER':  'RMSE [$\mathregular{gC~m^{-2}~day^{-1}}$]',
                    'LE':  'RMSE [$\mathregular{W~m^{-2}}$]',
                    'H':   'RMSE [$\mathregular{W~m^{-2}}$]'}

    fig, ax = plt.subplots(nrows=len(myDict), ncols=1, sharex=True, sharey=False, figsize=(9, 5*len(myDict)), constrained_layout=True)

    for ind, key in enumerate(myDict):

        ind_plot = np.arange(myDict[key]-365, myDict[key]) # change this to (0,365) for one variable, (365, 730) for two variables ...

        ax[ind].plot(np.arange(0,365), ds_plot[ind_plot,1], color='black')

        ax[ind].set_xlim([0,365])
        ax[ind].set_yscale('log')
        if(ylabel == 'RMSE'):
            ax[ind].set_ylabel(myDict_label[key])
        else:
            ax[ind].set_ylabel(ylabel)
        ax[ind].text(0.9, 0.93, key,  color='black', transform=ax[ind].transAxes, fontsize=18, bbox=dict(facecolor='white', edgecolor='white'))
        
        if (ind == len(myDict)-1):
            xtick_labels = True
        else:
            xtick_labels = False

    ax[0].text(0.02, 0.93, site + ' ' + title, color='black', transform=ax[0].transAxes, fontsize=18, bbox=dict(facecolor='white', edgecolor='white'))

    # Define the month format
    ax[len(myDict)-1].xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax[len(myDict)-1].xaxis.set_major_formatter(DateFormatter('%d-%b'))

    plt.savefig('../figures/'+ site + '_' + title + '_' + metric + '.png', bbox_inches='tight')

#----------------------------------------------------------
# open the results stored as a pickled file
os.chdir('../site_calib_outputs/')

surr_results = pk.load(open(options.site + '_' + options.crop + '_' + 'results_all.pk', 'rb'))

items = len(surr_results)

# Create an empty 2D Numpy array or matrix with 5 rows and 3 columns
rel_l2_val = np.empty((items, 2))
rmse_val   = np.empty((items, 2))
rrmse_val   = np.empty((items, 2))

for i in range(items):
    rel_l2_val[i,0] = i
    rmse_val[i,0]   = i
    rrmse_val[i,0]   = i
    if surr_results[i] is not None:
        rel_l2_val[i,1] = surr_results[i]['rel_l2_val']
        rmse_val[i,1]   = surr_results[i]['rmse_val']
        rrmse_val[i,1]  = surr_results[i]['rrmse_val']
    else:
        rel_l2_val[i,1] = np.nan
        rmse_val[i,1]   = np.nan
        rrmse_val[i,1]  = np.nan

myrc()

title=options.crop
site = options.site

plot_timeseries_subplots(rel_l2_val, site, title, ylabel='Relative surrogate error', metric='rel_l2')
plot_timeseries_subplots(rmse_val,   site, title, ylabel='RMSE',                     metric='rmse')
plot_timeseries_subplots(rrmse_val,  site, title, ylabel='Relative RMSE',            metric='rrmse')

#plot_timeseries(rel_l2_val[0:365, :],     site, title, varname='GPP', ylabel='Relative surrogate error', metric='rel_l2')
#plot_timeseries(rel_l2_val[365:730, :],   site, title, varname='ER',  ylabel='Relative surrogate error', metric='rel_l2')
#plot_timeseries(rel_l2_val[730:1095, :],  site, title, varname='LE',  ylabel='Relative surrogate error', metric='rel_l2')
#plot_timeseries(rel_l2_val[1095:1460, :], site, title, varname='H',   ylabel='Relative surrogate error', metric='rel_l2')

#plot_timeseries(rmse_val[0:365, :],       site, title, varname='GPP', ylabel='RMSE [$\mathregular{gC~m^{-2}~day^{-1}}$]', metric='rmse')
#plot_timeseries(rmse_val[365:730, :],     site, title, varname='ER',  ylabel='RMSE [$\mathregular{gC~m^{-2}~day^{-1}}$]', metric='rmse')
#plot_timeseries(rmse_val[730:1095, :],    site, title, varname='LE',  ylabel='RMSE [$\mathregular{W~m^{-2}}$]', metric='rmse')
#plot_timeseries(rmse_val[1095:1460, :],   site, title, varname='H',   ylabel='RMSE [$\mathregular{W~m^{-2}}$]', metric='rmse')

#plot_timeseries(rrmse_val[0:365, :],       site, title, varname='GPP', ylabel='Relative RMSE', metric='rrmse')
#plot_timeseries(rrmse_val[365:730, :],     site, title, varname='ER',  ylabel='Relative RMSE', metric='rrmse')
#plot_timeseries(rrmse_val[730:1095, :],    site, title, varname='LE',  ylabel='Relative RMSE', metric='rrmse')
#plot_timeseries(rrmse_val[1095:1460, :],   site, title, varname='H',   ylabel='Relative RMSE', metric='rrmse')

output = open(options.site + '_' + options.crop + '_' + '_' + 'rel_l2_rmse_rrmse_summary.txt','w')
output.write(title + '\n')
output.write('QoI'+ '\t' + 'Mean relative surrogate error' + '\t' + 'RMSE' + '\t' + 'Mean relative RMSE' + '\n')
output.write('GPP' + '\t' + str(round(np.nanmean(rel_l2_val[0:365, :],     axis=0)[1],4)) + '\t' + str(round(np.nanmean(rmse_val[0:365, :],     axis=0)[1],4)) + '\t' + str(round(np.nanmean(rrmse_val[0:365, :],     axis=0)[1],4)) + '\n')
output.write('ER'  + '\t' + str(round(np.nanmean(rel_l2_val[365:730, :],   axis=0)[1],4)) + '\t' + str(round(np.nanmean(rmse_val[365:730, :],   axis=0)[1],4)) + '\t' + str(round(np.nanmean(rrmse_val[365:730, :],   axis=0)[1],4)) + '\n')
output.write('LE'  + '\t' + str(round(np.nanmean(rel_l2_val[730:1095, :],  axis=0)[1],4)) + '\t' + str(round(np.nanmean(rmse_val[730:1095, :],  axis=0)[1],4)) + '\t' + str(round(np.nanmean(rrmse_val[730:1095, :],  axis=0)[1],4)) + '\n')
output.write('H'   + '\t' + str(round(np.nanmean(rel_l2_val[1095:1460, :], axis=0)[1],4)) + '\t' + str(round(np.nanmean(rmse_val[1095:1460, :], axis=0)[1],4)) + '\t' + str(round(np.nanmean(rrmse_val[1095:1460, :], axis=0)[1],4)) + '\n')
output.close()
