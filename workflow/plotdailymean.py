"""
Python modules for plotting time series
"""

import os
import matplotlib as mpl
mpl.use('Agg')
import numpy as np
import pandas as pd
import xarray as xr
from itertools import cycle

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter

from estaverage import estimate_daily_average_across_years

__author__ = 'Eva Sinha'
__email__  = 'eva.sinha@pnnl.gov'

plt.rc('figure', titlesize=15)
plt.rc('legend', fontsize=15)
plt.rc('axes',   labelsize=15, titlesize=15)
plt.rc('xtick',  labelsize=15)
plt.rc('ytick',  labelsize=15)
plt.rc('figure', figsize=(11, 8.5))

# ---------- function for estimating root mean square error ----------
def rmse(model, obs):
    return np.sqrt(((model - obs) ** 2).mean())

# ---------- function for estimating bias ----------
def bias(model, obs):
    return (model - obs).mean()

# ---------- function for estimating percent bias ----------
def per_bias(model, obs):
    return 100 * sum((model - obs))/sum(obs)

# ---------- function for estimating realtive root mean square error ----------
def rrmse(predictions, targets):
    rmse = np.sqrt(((predictions - targets) ** 2).mean())
    return rmse/np.sqrt((targets ** 2).mean())

#----------------------------------------------------------
def subplots_ts_valid_model_obs(ds_model, ds_obs, varnames, title, site, ylabel, conv_fact_model, conv_fact_obs, fname):
    """Plot timeseries from input xarray
        :param: ds_model:      model data xarray
        :param: ds_obs:        observation data xarray
        :param: varnames:      list of variable names of interest
        :param: title:        variable title for plotting
        :param: site:          site id for plotting
        :param: ylabel:        variable ylabel for plotting
        :param: conv_fact_model:   conversion factor for each variable for model data
        :param: conv_fact_obs:   conversion factor for each variable for observation data
        :param: fname:         file name prefix        
    """
    # Change directory
    os.chdir('../figures/')

    fig, ax = plt.subplots(nrows=len(varnames), ncols=1, sharex=True, sharey=False, figsize=(8, 5*len(varnames)), constrained_layout=True)

    for ind, var in enumerate(varnames):
    
        # Subset variable for plotting
        ds_model_plot = ds_model[var]
        ds_obs_plot   = ds_obs[var]
   
        if (var == 'EFLX_LH_TOT'):
            var = 'LE'
            ylabel[ind] = 'LE [$\mathregular{W~m^{-2}}$]'
        if (var == 'FSH'):
            var = 'H'
            ylabel[ind] = 'H [$\mathregular{W~m^{-2}}$]'
 
        # Scale by factor
        # for observational data convert from umol CO2 m-2 sec-1 to gC m-2 day-1  by multiplying by factor
        ds_model_plot = ds_model_plot / conv_fact_model[ind]
        ds_obs_plot   = ds_obs_plot * conv_fact_obs[ind]

        # 5 day rolling average
        ds_obs_roll   = ds_obs_plot.rolling(time=5, center=True).mean().dropna('time')

        # Estimate average across years for each day of the year
        ds_model_plot = ds_model_plot.groupby('time.dayofyear').mean('time')
        ds_obs_avg    = ds_obs_plot.groupby('time.dayofyear').mean('time')
 
        for yr in np.unique(ds_obs_roll['time.year']):
            ds_plot = ds_obs_roll.sel(time = str(yr))
            ax[ind].plot(ds_plot.time.dt.dayofyear, ds_plot, color='darkgrey', linewidth=0.5)
        ax[ind].plot(ds_obs_avg,   color='black', linewidth=1.0, label='Mean observation')
        ax[ind].plot(ds_model_plot, color='red', linewidth=1.0, label='Modeled')

        ax[ind].set_ylabel(ylabel[ind])
        ax[ind].set_xlim([0,365])

        ax[ind].text(0.75, 0.85, 'RRMSE '+ str(rrmse(ds_model_plot, ds_obs_avg).values.round(decimals=2)), color='black', transform=ax[ind].transAxes, fontsize=18, bbox=dict(facecolor='white', edgecolor='white'))
 
    ax[len(varnames)-1].legend(loc='upper left')
    ax[0].text(0.02, 0.93, title.capitalize(), color='black', transform=ax[0].transAxes, fontsize=18, bbox=dict(facecolor='white', edgecolor='white'))
    ax[0].text(0.85, 0.93, site,  color='black', transform=ax[0].transAxes, fontsize=18, bbox=dict(facecolor='white', edgecolor='white'))

    # Define the month format
    ax[len(varnames)-1].xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax[len(varnames)-1].xaxis.set_major_formatter(DateFormatter('%d-%b'))

    plt.savefig(fname + '_valid_model_obs.png', bbox_inches='tight')

    plt.close(fig)

    # Change directory    
    os.chdir('../workflow/')

#----------------------------------------------------------
def subplots_ts_monthly_valid_model_obs(ds_model, ds_obs, varnames, title, site, ylabel, conv_fact_model, conv_fact_obs, fname):
    """Plot timeseries from input xarray
        :param: ds_model:      model data xarray
        :param: ds_obs:        observation data xarray
        :param: varnames:      list of variable names of interest
        :param: title:        variable title for plotting
        :param: site:          site id for plotting
        :param: ylabel:        variable ylabel for plotting
        :param: conv_fact_model:   conversion factor for each variable for model data
        :param: conv_fact_obs:   conversion factor for each variable for observation data
        :param: fname:         file name prefix
    """
    # Change directory
    os.chdir('../figures/')

    # Plot model and observations
    fig, ax = plt.subplots(nrows=len(varnames), ncols=1, sharex=True, sharey=False, figsize=(8, 5*len(varnames)), constrained_layout=True)

    for ind, var in enumerate(varnames):

        # Subset variable for plotting
        ds_model_plot = ds_model[var]
        ds_obs_plot   = ds_obs[var]

        if (var == 'EFLX_LH_TOT'):
            var = 'LE'
            ylabel[ind] = 'LE [$\mathregular{W~m^{-2}}$]'
        if (var == 'FSH'):
            var = 'H'
            ylabel[ind] = 'H [$\mathregular{W~m^{-2}}$]'

        # Estimate monthly mean for energy fluxes
        if (var in ['GPP', 'ER']):
           ds_model_plot = ds_model_plot.resample(time='1M', skipna=False).sum(skipna=False)
           ds_obs_plot   = ds_obs_plot.resample(time='1M', skipna=False).sum(skipna=False)
        if (var in ['LE', 'H']):
           ds_model_plot = ds_model_plot.resample(time='1M', skipna=False).mean()
           ds_obs_plot   = ds_obs_plot.resample(time='1M', skipna=False).mean()

        # Scale by factor
        # for observational data convert from umol CO2 m-2 sec-1 to gC m-2 day-1  by multiplying by factor
        ds_model_plot = ds_model_plot / conv_fact_model[ind]
        ds_obs_plot   = ds_obs_plot * conv_fact_obs[ind]

        # Estimate average across years for each day of the year
        ds_model_plot = ds_model_plot.groupby('time.dayofyear').mean('time')
        ds_obs_avg   = ds_obs_plot.groupby('time.dayofyear').mean('time')

        for yr in np.unique(ds_obs_plot['time.year']):
            ds_plot = ds_obs_plot.sel(time = str(yr))
            ax[ind].plot(ds_plot.time.dt.dayofyear, ds_plot, color='darkgrey', marker='o', linewidth=0.5)
        ax[ind].plot(ds_obs_avg.dayofyear, ds_obs_avg,   color='black', marker='o', linewidth=1.0, label='Mean observation')
        ax[ind].plot(ds_model_plot.dayofyear, ds_model_plot, color='red', marker='o', linewidth=1.0, label='Modeled')

        ax[ind].set_ylabel(ylabel[ind])
        ax[ind].set_xlim([0,365])

        ax[ind].text(0.75, 0.85, 'RRMSE '+ str(rrmse(ds_model_plot, ds_obs_avg).values.round(decimals=2)), color='black', transform=ax[ind].transAxes, fontsize=18, bbox=dict(facecolor='white', edgecolor='white'))

    ax[len(varnames)-1].legend(loc='upper left')
    ax[0].text(0.02, 0.93, title.capitalize(), color='black', transform=ax[0].transAxes, fontsize=18, bbox=dict(facecolor='white', edgecolor='white'))
    ax[0].text(0.85, 0.93, site,  color='black', transform=ax[0].transAxes, fontsize=18, bbox=dict(facecolor='white', edgecolor='white'))

    # Define the month format
    ax[len(varnames)-1].xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax[len(varnames)-1].xaxis.set_major_formatter(DateFormatter('%d-%b'))

    plt.savefig(fname + '_monthly_valid_model_obs.png', bbox_inches='tight')

    plt.close(fig)

    # Change directory    
    os.chdir('../workflow/')

#----------------------------------------------------------
def plot_ts_valid_lai(ds_model, var, obs_data, plot_col, ylabel, title, site, fname):
    """Plot timeseries from input xarray
        :param: ds_model:      model data xarray
        :param: obs_data:        observation data pandas dataframe
        :param: title:        variable title for plotting
        :param: site:          site id for plotting
        :param: fname:         file name prefix
    """
    # Change directory
    os.chdir('../figures/')

    # Plot model and observations
    fig, ax = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=False, figsize=(8, 5), constrained_layout=True)

    # Estimate average across years for each day of the year
    ds_model_avg = estimate_daily_average_across_years(ds_model)
    ds_model     = ds_model[var]
    ds_model_avg = ds_model_avg[var]

    for yr in np.unique(ds_model['time.year']):
        ds_plot = ds_model.sel(time = str(yr))
        plt.plot(ds_plot.time.dt.dayofyear, ds_plot, color='darkgrey', linewidth=0.5)
    ax.plot(ds_model_avg, color='black',     linewidth=1.0, label='Model mean')

    groups = obs_data.groupby('Year')
    for name, group in groups:
        ax.plot(group.DayofYear, group[plot_col], marker='o', linestyle='', markersize=8, label=name)

    ax.set_ylabel(ylabel)
    ax.set_xlim([0,365])

    ax.legend(loc='lower left')
    ax.text(0.02, 0.93, title.capitalize(), color='black', transform=ax.transAxes, fontsize=18, bbox=dict(facecolor='white', edgecolor='white'))
    ax.text(0.85, 0.93, site,  color='black', transform=ax.transAxes, fontsize=18, bbox=dict(facecolor='white', edgecolor='white'))

    # Define the month format
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax.xaxis.set_major_formatter(DateFormatter('%d-%b'))

    plt.savefig(fname, bbox_inches='tight')

    plt.close(fig=None)

    # Change directory    
    os.chdir('../workflow/')

#----------------------------------------------------------
def plot_valid_CRPYLD(ds_model, obs_data, plot_col, ylabel, title, site, fname):
    """Plot timeseries from input xarray
        :param: ds_model:      model data xarray
        :param: obs_data:        observation data pandas dataframe
        :param: title:        variable title for plotting
        :param: site:          site id for plotting
        :param: fname:         file name prefix
    """
    # Change directory
    os.chdir('../figures/')

    # Plot model and observations
    fig, ax = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=False, figsize=(8, 5), constrained_layout=True)

    ax.boxplot(ds_model[plot_col])
    ax.set_xticks([1])
    ax.set_xticklabels([title.capitalize()])
    groups = obs_data.groupby('Year')
    for name, group in groups:
        if(plot_col == 'CRPYLD'):
            ax.scatter(1, group.harvest_bu_acre, marker='o', label=name)
        if(plot_col == 'growing_season'):
            ax.scatter(1, group.growing_season, marker='o', label=name)

    ax.legend(loc='lower left')
    ax.set_ylabel(ylabel)

    ax.text(0.02, 0.93, title.capitalize(), color='black', transform=ax.transAxes, fontsize=18, bbox=dict(facecolor='white', edgecolor='white'))
    ax.text(0.85, 0.93, site,  color='black', transform=ax.transAxes, fontsize=18, bbox=dict(facecolor='white', edgecolor='white'))

    plt.savefig(fname, bbox_inches='tight')

    plt.close(fig=None)

    # Change directory    
    os.chdir('../workflow/')
