"""
Python modules for plotting time series
"""

import os
import matplotlib as mpl 
mpl.use('agg')
import pandas as pd
import numpy as np
import xarray as xr
import pickle

import matplotlib.pyplot as plt 
import cartopy.crs as ccrs
import cartopy.feature as cfeature

__author__ = 'Eva Sinha'
__email__  = 'eva.sinha@pnnl.gov'

from util_spatial_plots import *

# -----------------------------------------------------------
def create_region_da(da):
    """Create an xarray containing region locations
    :param: da:      xarray
    """

    da = da.assign_coords({'lsmlon': np.unique(da['LONGXY'])})
    da = da.assign_coords({'lsmlat': np.unique(da['LATIXY'])})

    lat  = da.lsmlat
    lon  = da.lsmlon

    nlat = len(lat.values)
    nlon = len(lon.values)

    # Create empty gridded array
    composite_grid = np.empty([nlat, nlon])

    # Adding dimensions and coordinates
    composite_grid = xr.DataArray(composite_grid, dims=('lat', 'lon'))
    composite_grid = composite_grid.assign_coords(lat=lat.values, lon=lon.values)
    composite_grid.name = 'Region'

    # Dictionary for subregions
    myDict_region = {'Set1': 'Northern_Rockies',
                     'Set2': 'Upper_Midwest',
                     'Set3': 'Ohio_Valley'}

    pickle_fname = '/qfs/people/sinh210/wrk/E3SM_SFA/ELM-Bioenergy/spatial_plots/figures/domain.lnd.Northern_Rockies_cruncep_c220216.out'

    #iterate through dictionary
    for i, key in enumerate(myDict_region):
    
        # load pickle to read lon_lat coordinates for three sets
        notnull_coords = pickle.load(open(pickle_fname.replace('Northern_Rockies', myDict_region[key]), 'rb'))

        for lon, lat in notnull_coords:
            composite_grid.loc[lat, lon] = i

    return composite_grid

#----------------------------------------------------------

# Read observational site lat and lon
site_loc = pd.read_csv('site_loc.csv')

fpath = '/compyfs/sinh210/mygetregionaldata/' 
fname = 'surfdata_20x34pt_f19_US_Midwest_sub_cru_50pfts_simyr1850_c220216.nc'

# Open a netcdf domain dataset
da = xr.open_dataset(fpath + fname)

# Create an xarray containing region locations
composite_grid = create_region_da(da)

# Subset sites that have carbon flux data
# Make plot showing regions and location of Ameriflux sites
xr_plot(composite_grid, cbar_label='Region', fname='fig_Regions.png', xy_df=site_loc[site_loc['carbon_flux'] == True])

# Subset sites that don't have carbon flux data
# Make plot showing regions and location of Ameriflux sites
xr_plot(composite_grid, cbar_label='Region', fname='fig_Regions_additional.png', xy_df=site_loc[site_loc['carbon_flux'] == False])

# Make plot showing regions and location of Ameriflux sites
xr_plot(composite_grid, cbar_label='Region', fname='fig_Regions_all_sites.png', xy_df=site_loc)
