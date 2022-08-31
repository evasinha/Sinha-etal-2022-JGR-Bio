import os
import numpy as np
import pandas as pd
import xarray as xr
from optparse import OptionParser

from estaverage import estimate_daily_average_across_years
from plotdailymean import *

__author__ = 'Eva Sinha'
__email__  = 'eva.sinha@pnnl.gov'

parser = OptionParser();

parser.add_option("--site", dest="site", default="", \
                  help="Site ID")
parser.add_option("--crop", dest="crop", default="", \
                  help="Modeled crop name")
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

# List of variable names that we want to keep
varnames = ['GPP', 'ER', 'EFLX_LH_TOT', 'FSH']

# Read names of output variables and conversion factor
rotation_yrs = pd.read_csv('../info_obsdata/' + options.site + '_corn_soybean_rotation_years.csv', comment='#')
crop_yrs     = rotation_yrs[options.crop].dropna().astype(int)

# Read ELM validation model output for specified case and year range and subset for variables
ds_model = read_valid_model_data(options.rundir, options.caseid, crop_yrs, varnames)

# Open a netcdf containing observed data
ds_obs = xr.open_dataset('/home/ac.eva.sinha/ELM-Bioenergy/timeseries_plots/' + options.obsdir + options.obsfname)

# Read list of validation years for the site
valid_yrs = pd.read_csv('../info_obsdata/' + options.site + '_validation_years.csv', comment='#')
valid_yrs = valid_yrs[options.crop].dropna().astype(int)

# Only keep observational data for validation years
ds_obs = ds_obs.sel(time = ds_obs.time.dt.year.isin(valid_yrs))

# Create array of ylabel for each plot
ylabel = ['GPP [$\mathregular{gC~m^{-2}~day^{-1}}$]', 'ER [$\mathregular{gC~m^{-2}~day^{-1}}$]', \
          'EFLX_LH_TOT [$\mathregular{W~m^{-2}}$]', 'FSH [$\mathregular{W~m^{-2}}$]']

# Title for plot
title = options.crop
site  = options.site

# Conversion constants
CONV_umolCO2_gC = 1.03775
CONV_SEC_DAY    = 1 / (24 * 60 * 60)

conv_fact_model = [CONV_SEC_DAY, CONV_SEC_DAY, 1, 1]
conv_fact_obs   = [CONV_umolCO2_gC, CONV_umolCO2_gC, 1, 1]

subplots_ts_valid_model_obs(ds_model, ds_obs, varnames, title, site, ylabel, conv_fact_model, conv_fact_obs, fname=options.fnamepre)
ylabel = ['GPP [$\mathregular{gC~m^{-2}~month^{-1}}$]', 'ER [$\mathregular{gC~m^{-2}~month^{-1}}$]', \
          'EFLX_LH_TOT [$\mathregular{W~m^{-2}}$]', 'FSH [$\mathregular{W~m^{-2}}$]']
subplots_ts_monthly_valid_model_obs(ds_model, ds_obs, varnames, title, site, ylabel, conv_fact_model, conv_fact_obs, fname=options.fnamepre)

if(options.site == 'US-UiC'):
   fpath = '/home/ac.eva.sinha/ELM-Bioenergy/obsdata/UIUCEnergyFarm/'
else:
   fpath = '/home/ac.eva.sinha/ELM-Bioenergy/obsdata/AmeriFlux/'

# ---------- LAI ----------
# Read ELM validation model output for specified case and year range and subset for variables
var      = 'TLAI'
ds_model = read_valid_model_data(options.rundir, options.caseid, crop_yrs, varnames=[var])

fname = options.site + '_LAI.csv'

# Site observations file path and file name
obs_data = pd.read_csv(fpath + fname)

# Since LAI and harvest were never used for calibration observed LAI and harvest for all years is shown
# Only keep observational data for validation years
#obs_data = obs_data[(obs_data.Year.isin(valid_yrs)) & (obs_data.Site == site) & (obs_data.Crop == options.crop)]
obs_data = obs_data[(obs_data.Site == site) & (obs_data.Crop == options.crop)]

plot_col = 'LAI_avg'
ylabel = 'TLAI'

plot_ts_valid_lai(ds_model, var, obs_data, plot_col, ylabel, title, site, fname=options.fnamepre+ '_valid_lai.png')

# ---------- Canopy height ----------
# Read ELM validation model output for specified case and year range and subset for variables
var      = 'HTOP'
ds_model = read_valid_model_data(options.rundir, options.caseid, crop_yrs, varnames=[var])

fname = options.site + '_canopy_height.csv'

# Site observations file path and file name
obs_data = pd.read_csv(fpath + fname)

# Since LAI and harvest were never used for calibration observed LAI and harvest for all years is shown
# Only keep observational data for validation years
#obs_data = obs_data[(obs_data.Year.isin(valid_yrs)) & (obs_data.Site == site) & (obs_data.Crop == options.crop)]
obs_data = obs_data[(obs_data.Site == site) & (obs_data.Crop == options.crop)]

plot_col = 'canopy_height'
ylabel   = 'Canopy height [m]'
plot_ts_valid_lai(ds_model, var, obs_data, plot_col, ylabel, title, site, fname=options.fnamepre+ '_valid_canopy_height.png')

# ---------- Harvest ----------
# Read ELM model output for specified case and year range and subset for variables
ds_model = read_valid_model_data(options.rundir, options.caseid, crop_yrs, varnames=['CRPYLD'])

# Convert to pandas dataframe for writing csv file
df_model = ds_model.to_dataframe()

# Estimate maximum yield for each year
model_dmyield = df_model.groupby(df_model.index.year).max()

# Save to csv file
model_dmyield.to_csv('../figures/' + options.fnamepre + '_CRPYLD.csv', index_label='Year')

fname = options.site + '_harvest.csv'

# Site observations file path and file name
obs_data = pd.read_csv(fpath + fname)

# Since LAI and harvest were never used for calibration we can show observed LAI and harvest for all years
# Only keep observational data for validation years
# obs_data = obs_data[(obs_data.Year.isin(valid_yrs)) & (obs_data.Site == site) & (obs_data.Crop == options.crop)]
obs_data = obs_data[(obs_data.Site == site) & (obs_data.Crop == options.crop)]

plot_col = 'CRPYLD'
ylabel = 'Harvest [$\mathregular{bu~acre^{-1}}$]'

plot_valid_CRPYLD(model_dmyield, obs_data, plot_col, ylabel, title, site, fname=options.fnamepre+'_valid_harv.png')

# ---------- Growing season ----------
# Read ELM model output for specified case and year range and subset for variables
ds_model_plant = read_valid_model_data(options.rundir, options.caseid, crop_yrs, varnames=['PLANTDAY'])
ds_model_harv  = read_valid_model_data(options.rundir, options.caseid, crop_yrs, varnames=['HARVESTDAY'])

# For harvest date first subset for months of Sept-Oct and then estimate minimum (999 is default value before harvest)
ds_model_harv = ds_model_harv.sel(time = ds_model_harv.time.dt.month.isin([9, 10, 11, 12]))
df_model_harv = ds_model_harv.groupby('time.year').min(dim='time').to_dataframe().reset_index()

# For plant date estimate minimum for each year (999 is default value before planting)
df_model_plant = ds_model_plant.groupby('time.year').min(dim='time').to_dataframe().reset_index()

# Merge into a single pandas dataframe
df_model_dates = df_model_harv.merge(df_model_plant, left_on='year', right_on='year')
# Estimating growing season length
df_model_dates['growing_season'] = df_model_dates['HARVESTDAY']- df_model_dates['PLANTDAY']

fname = options.site + '_planting_harvest_days.csv'

# Site observations file path and file name
obs_data = pd.read_csv(fpath + fname)

# Since LAI and harvest were never used for calibration we can show observed LAI and harvest for all years
# Only keep observational data for validation years
# obs_data = obs_data[(obs_data.Year.isin(valid_yrs)) & (obs_data.Site == site) & (obs_data.Crop == options.crop)]
obs_data = obs_data[(obs_data.Site == site) & (obs_data.Crop == options.crop)]

plot_col = 'growing_season'
ylabel   = 'Growing season length [days]'

plot_valid_CRPYLD(df_model_dates, obs_data, plot_col, ylabel, title, site, fname=options.fnamepre+ '_valid_growing_season.png')
