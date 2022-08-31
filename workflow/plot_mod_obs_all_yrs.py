import os
import numpy as np
import pandas as pd
import xarray as xr
import seaborn as sns
from optparse import OptionParser

import matplotlib.pyplot as plt

__author__ = 'Eva Sinha'
__email__  = 'eva.sinha@pnnl.gov'

plt.rc('figure', titlesize=20)
plt.rc('legend', fontsize=20)
plt.rc('axes',   labelsize=20, titlesize=20)
plt.rc('xtick',  labelsize=20)
plt.rc('ytick',  labelsize=20)

parser = OptionParser();

parser.add_option("--site", dest="site", default="", \
                  help="Site ID")
parser.add_option("--rundir", dest="rundir", default="", \
                  help="Directory where ELM ensemble outputs are stored")
parser.add_option("--caseid", dest="caseid", default="", \
                  help="Case name")
parser.add_option("--obsdir", dest="obsdir", default="", \
                  help="Directory where netcdf file containing observed data is stored")
parser.add_option("--obsfname", dest="obsfname", default="", \
                  help="File name containing observation data")
parser.add_option("--fnamepre", dest="fnamepre", default="", \
                  help="file name prefix for saving comparison plots")

(options, args) = parser.parse_args()

#----------------------------------------------------------
def read_valid_model_data(rundir, caseid, crop_yrs, varnames):
    """Read ELM validation model output for all ensemble members for specified case and year range and subset for variables
    :param: rundir:     path to the run directory
    :param: caseid:     case name
    :param: crop_yrs:   crop years for reading data
    :param: varnames:   list of variable names of interest
    :return:            single data array containing validation model results for select years and variables
    """

    # Read names of all NetCDF files within the given year range
    fnames = []
    for yr in crop_yrs:
        fnames.append(rundir + '/' + caseid + '.elm.h0.' + str(yr) + '-01-01-00000.nc')

    # Open a multiple netCDF data file and load the data into xarrays
    with xr.open_mfdataset(fnames, concat_dim='time') as ds: 

        # Drop landgrid dimension
        ds = ds.isel(lndgrid=0)

        # Only keep select variables in the data array
        ds = ds[varnames]

    return (ds)

#----------------------------------------------------------
def plot_ts_model_obs_all_yrs(ds_model, ds_obs, varnames, site, ylabel, conv_fact_model, conv_fact_obs, fname):
    """Plot timeseries from input xarray
        :param: ds_model:      model data xarray
        :param: ds_obs:        observation data xarray
        :param: varnames:      list of variable names of interest
        :param: ylabel:        variable ylabel for plotting
        :param: fname:         file name prefix        
    """
    # Plot model and observations
    parameters = {'figure.titlesize':20,
                  'figure.figsize' : (17, 8.5)}
    
    plt.rcParams.update(parameters)

    # Change directory
    os.chdir('../figures/')

    for ind, var in enumerate(varnames):
    
        # Subset variable for plotting
        ds_model_plot = ds_model[var]
        ds_obs_plot   = ds_obs[var]

        # Scale by factor. 
        # for observational data convert from umol CO2 m-2 sec-1 to gC m-2 day-1  by multiplying by factor
        ds_model_plot = ds_model_plot / conv_fact_model[ind]
        ds_obs_plot   = ds_obs_plot * conv_fact_obs[ind]

        # Convert CFTimeIndex to DatetimeIndex
        # This will ensure that both observations and modeled have same time units
        # https://stackoverflow.com/questions/55786995/converting-cftime-datetimejulian-to-datetime
        datetimeindex = ds_model_plot.indexes['time'].to_datetimeindex()
        ds_model_plot['time'] = datetimeindex

        fig, ax = plt.subplots()
        ds_model_plot.plot(ax=ax, color='black', linewidth=1.0, label='Modeled')
        ds_obs_plot.plot(ax=ax, color='red',   linewidth=1.0, label='Observed')
        
        plt.ylabel(ylabel[ind])
        plt.xlabel('')
        plt.legend(loc='upper left')

        ax.text(0.90, 0.95, site,  color='black', transform=ax.transAxes, fontsize=18, bbox=dict(facecolor='white', edgecolor='white'))
 
        plt.savefig(fname + '_' +  var + '_all_years.pdf', bbox_inches='tight')

        plt.close(fig)

    # Change directory
    os.chdir('../workflow/')

#----------------------------------------------------------
def plot_annual_barplot(ds_model, ds_obs, soybean_yrs, varnames, site, ylabel, conv_fact_model, conv_fact_obs, fname):
    """Plot timeseries with and without rotation from input xarray
        :param: ds_model:      model data xarray
        :param: ds_obs:        observation data xarray
        :param: varnames:      list of variable names of interest
        :param: fname:         file name prefix        
    """
    # Plot model and observations
    parameters = {'figure.titlesize':20,
                  'figure.figsize' : (17, 8.5)}
    
    plt.rcParams.update(parameters)

    # Change directory
    os.chdir('../figures/')

    for ind, var in enumerate(varnames):
  
        if (var == 'GPP'):
           # Subset variable for plotting
           ds_model = ds_model[var]
           ds_obs   = ds_obs[var]

           # Scale by factor. 
           ds_model = ds_model / conv_fact_model[ind]
           ds_obs   = ds_obs / conv_fact_obs[ind]

           # Estimate annual average
           ds_model_annual = ds_model.groupby('time.year').sum(dim='time', skipna=False)  # Annual
           ds_obs_annual   = ds_obs.groupby('time.year').sum(dim='time')  # Annual

           # Rename dataarray
           ds_model_annual = ds_model_annual.rename(var)
           ds_obs_annual   = ds_obs_annual.rename(var)

           # Convert to pandas series
           ds_model_annual = ds_model_annual.to_dataframe()
           ds_obs_annual   = ds_obs_annual.to_dataframe()

           # Add new column to specify crop rotation
           ds_model_annual['Desc'] = 'Modeled'
           ds_obs_annual['Desc']   = 'Observed'

           # Row bind into a single data frame
           data_plot = pd.concat([ds_model_annual, ds_obs_annual])
           data_plot = data_plot.reset_index()

           # Replace zero with nan
           data_plot['GPP'] = data_plot['GPP'].replace({'0':np.nan, 0:np.nan})

           # Drop na
           data_plot = data_plot.dropna()

           # Add crop name
           data_plot['Crop']  = 'Corn'
           data_plot.loc[data_plot['year'].isin(soybean_yrs), 'Crop'] = 'Soybean'

           # Sort data
           data_plot = data_plot.sort_values(by=['year', 'Crop'])

           col_palette = {'Observed':'silver', 'Modeled':'tomato'}

           plt.xlim(-0.5, 13.5)

           # ----- Make bar plot -----
           g = sns.barplot(data=data_plot, x='year', y='GPP', hue='Desc', palette=col_palette)

           # Modify axis labels
           g.set(xlabel='', ylabel='GPP [$\mathregular{gC~m^{-2}~year^{-1}}$]')

           # Insert background shading
           for i in range(0, 14, 2):
             plt.axvspan(i-0.5, i+.5, facecolor='yellow', alpha=0.15, zorder=-100)
           for i in range(1, 14, 2):
             plt.axvspan(i-0.5, i+.5, facecolor='cyan', alpha=0.15, zorder=-100)

           # Add hatching pattern
           #pattern = ['x', '/']
           #hatches = np.tile(pattern,14)

           #for pat,bar in zip(hatches, g.patches):
           #   bar.set_hatch(pat)

           # Move legend to bottom
           sns.move_legend(g, 'upper left', title=None)

           g.text(0.90, 0.95, site,  color='black', transform=g.transAxes, fontsize=20, bbox=dict(facecolor='white', edgecolor='white'))

           plt.savefig(fname + '_annual_' +  var + '.png', bbox_inches='tight')

           plt.close(fig=None)

           # ----- Make box plot -----
           g = sns.boxplot(data=data_plot, x='Crop', y='GPP', hue='Desc', palette=col_palette, width=0.5)

           # Modify axis labels
           g.set(xlabel='', ylabel='GPP [$\mathregular{gC~m^{-2}~year^{-1}}$]')

           # Move legend to bottom
           sns.move_legend(g, 'lower left', title=None)

           g.text(0.90, 0.95, site,  color='black', transform=g.transAxes, fontsize=20, bbox=dict(facecolor='white', edgecolor='white'))

           plt.savefig(fname + '_annual_boxplot' +  var + '.png', bbox_inches='tight')

           plt.close(fig=None)

    # Change directory
    os.chdir('../workflow/')

#----------------------------------------------------------

# List of variable names that we want to keep
varnames = ['GPP', 'ER', 'EFLX_LH_TOT', 'FSH']

# Read rotation years and combine all years for corn and soybean in a single list
rotation_yrs = pd.read_csv('../info_obsdata/' + options.site + '_corn_soybean_rotation_years.csv', comment='#')
crop_yrs = rotation_yrs['corn'].dropna().astype(int).to_list() + \
           rotation_yrs['soybean'].dropna().astype(int).to_list()

soybean_yrs = rotation_yrs['soybean'].dropna().astype(int).to_list()

# Read ELM validation model output for specified case and year range and subset for variables
ds_model = read_valid_model_data(options.rundir, options.caseid, crop_yrs, varnames)

# Open a netcdf containing observed data (keep data for all years)
ds_obs = xr.open_dataset('/home/ac.eva.sinha/ELM-Bioenergy/timeseries_plots/' + options.obsdir + options.obsfname)

# Create array of ylabel for each plot
ylabel = ['GPP [$\mathregular{gC~m^{-2}~day^{-1}}$]', 'ER [$\mathregular{gC~m^{-2}~day^{-1}}$]', \
'EFLX_LH_TOT [$\mathregular{W~m^{-2}}$]', 'FSH [$\mathregular{W~m^{-2}}$]']

# Title for plot
site  = options.site

# Conversion constants
CONV_umolCO2_gC = 1.03775
CONV_SEC_DAY    = 1 / (24 * 60 * 60)

conv_fact_model = [CONV_SEC_DAY, CONV_SEC_DAY, 1, 1]
conv_fact_obs   = [CONV_umolCO2_gC, CONV_umolCO2_gC, 1, 1]

plot_ts_model_obs_all_yrs(ds_model, ds_obs, varnames, site, ylabel, conv_fact_model, conv_fact_obs, fname=options.fnamepre)

plot_annual_barplot(ds_model, ds_obs, soybean_yrs, varnames, site, ylabel, conv_fact_model, conv_fact_obs, fname=options.fnamepre)
