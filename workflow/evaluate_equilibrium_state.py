"""
Python modules for making spatial plots of ELM outputs
"""
import os
import sys
import matplotlib as mpl
mpl.use('Agg')
import numpy as np
import xarray as xr
from datetime import timedelta

__author__ = 'Eva Sinha'
__email__  = 'eva.sinha@pnnl.gov'

from util_vector_plots import *
from util_read_data import *
#------------------------------------

# Dictionary containing units
myDict_units = {'GPP':       'GPP [gC/m2/year]',
                'ER':        'ER [gC/m2/year]',
                'NEE':       'NEE [gC/m2/year]',
                'NPP':       'NPP [gC/m2/year]',
                'NBP':       'NBP [gC/m2/year]',
                'TOTECOSYSC':'TOTECOSYSC [gC/m2]',
                'TOTSOMC':   'TOTSOMC [gC/m2]'}

# List of variable names that we want to keep
varnames = ['NEE', 'NPP', 'NBP', 'GPP', 'TOTECOSYSC', 'TOTSOMC']

yr_start = 1
yr_end   = 220
yr_step  = 20

caseid_ad_spinup    = '20230114_20x34_corn_soy_rot_US-Ne3_param_ELM_USRDAT_ICBELMCNCROP_ad_spinup'
caseid_final_spinup = '20230114_20x34_corn_soy_rot_US-Ne3_param_ELM_USRDAT_ICBELMCNCROP'

# Read ELM model output for ad spinup
mon_day_str = '-01-01'
fpath = '/compyfs/sinh210/e3sm_scratch/' + caseid_ad_spinup + '/run/'
ds_model_ad_spinup = read_spinup_model_output(yr_start, yr_end, yr_step, fpath, caseid_ad_spinup, mon_day_str, varnames, decode_times=False)
ds_model_ad_spinup['time'] = ds_model_ad_spinup['time']/365

# Read ELM model output for final spinup
fpath = '/compyfs/sinh210/e3sm_scratch/' + caseid_final_spinup + '/run/'
ds_model_final_spinup = read_spinup_model_output(yr_start+20, yr_end, yr_step, fpath, caseid_final_spinup, mon_day_str, varnames, decode_times=False)

# Shift final spinup time
ds_model_final_spinup['time'] = ds_model_final_spinup['time']/365 + 200

# Merge ad and final spinups
ds_model_merge = xr.merge([ds_model_ad_spinup, ds_model_final_spinup])

# Scale by conversion factor
for ind, var in enumerate(varnames):
   ds_model_merge[var] = ds_model_merge[var]/conv_factor[var]

# Convert to pandas dataframe
site_data = [{'SiteID':'US-Ne3', 'lat':41.1651, 'lon':263.5234},
             {'SiteID':'US-Ro1', 'lat':44.7143, 'lon':266.9102},
             {'SiteID':'US-UiC', 'lat':40.0647, 'lon':271.8017}]

site_data = pd.DataFrame(data = site_data)

for ind, row in site_data.iterrows():

   # Interpolate values for the site
   ds_plot = ds_model_merge.interp(lat=row['lat'], lon=row['lon']).to_array()

   ds_plot.coords['SiteID'] = row['SiteID']

   if(ind == 0):
      ds_plot_merge = ds_plot
   else:
      ds_plot_merge = xr.concat([ds_plot_merge, ds_plot], dim='SiteID')

   # Make plot evaluting whether equilibrium is reached for the site
   xarray_facet_line_plot(ds_plot, facet_col='variable', \
                          xlabel='', ylabel='', fname='Equilibrium_check_'+row['SiteID']+'.png', \
                          xmin=0, xmax=400, xvline=yr_end, sharey=False)

# Extract variable names and replace with variable name and units
varnames = ds_plot_merge['variable'].values

for ind, var in enumerate(varnames):
   varnames[ind] = myDict_units[var]

ds_plot_merge['variable'] = varnames

xarray_facet_grid_line_plot(ds_plot_merge, facet_row='variable', facet_col='SiteID',\
                            xvline=yr_end, xlabel='', ylabel='', fname='Equilibrium_check.png')
