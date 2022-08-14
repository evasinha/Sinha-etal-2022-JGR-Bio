import numpy as np
import pandas as pd
import xarray as xr
import pickle

__author__ = 'Eva Sinha'
__email__  = 'eva.sinha@pnnl.gov'

from util_myDict_labels import *

#----------------------------------------------------------
def create_composite_grid(da_merge, varname):
    """Create a composite grid by merging certain regions from each set
    :param: da_merge:      xarray
    :param: varname:       variable of interest
    """

    lat  = da_merge.lat
    lon  = da_merge.lon

    nlat = len(lat.values)
    nlon = len(lon.values)

    # Create empty gridded array
    composite_grid = np.empty([nlat, nlon])

    # Adding dimensions and coordinates
    composite_grid = xr.DataArray(composite_grid, dims=('lat', 'lon'))
    composite_grid = composite_grid.assign_coords(lat=lat.values, lon=lon.values)
    composite_grid.name = varname

    pickle_fname = '/qfs/people/sinh210/wrk/E3SM_SFA/ELM-Bioenergy/spatial_plots/figures/domain.lnd.Northern_Rockies_cruncep_c220216.out'

    # Dictionary for subregions
    myDict_region = {'Set1': 'Northern_Rockies',
                     'Set2': 'Upper_Midwest',
                     'Set3': 'Ohio_Valley'}

    #iterate through dictionary
    for i, key in enumerate(myDict_region):
    
        # load pickle to read lon_lat coordinates for three sets
        notnull_coords = pickle.load(open(pickle_fname.replace('Northern_Rockies', myDict_region[key]), 'rb'))

        for lon, lat in notnull_coords:
            composite_grid.loc[lat, lon] = da_merge[varname].sel(Set=key, lat=lat, lon=lon)

    composite_grid = composite_grid.expand_dims(Set = ['Composite'])
    
    return composite_grid
 
#----------------------------------------------------------
def create_no_rot_composite_grid(da_merge, varname):
    """Create a composite grid by merging certain regions from each set
    :param: da_merge:      xarray
    :param: varname:       variable of interest
    """

    lat  = da_merge.lat
    lon  = da_merge.lon

    nlat = len(lat.values)
    nlon = len(lon.values)

    # Create empty gridded array
    composite_grid = np.empty([nlat, nlon])

    # Adding dimensions and coordinates
    composite_grid = xr.DataArray(composite_grid, dims=('lat', 'lon'))
    composite_grid = composite_grid.assign_coords(lat=lat.values, lon=lon.values)
    composite_grid.name = varname

    pickle_fname = '/qfs/people/sinh210/wrk/E3SM_SFA/ELM-Bioenergy/spatial_plots/figures/domain.lnd.Northern_Rockies_cruncep_c220216.out'

    # Dictionary for subregions
    myDict_region = {'Set1_no_rot': 'Northern_Rockies',
                     'Set2_no_rot': 'Upper_Midwest',
                     'Set3_no_rot': 'Ohio_Valley'}

    #iterate through dictionary
    for i, key in enumerate(myDict_region):
    
        # load pickle to read lon_lat coordinates for three sets
        notnull_coords = pickle.load(open(pickle_fname.replace('Northern_Rockies', myDict_region[key]), 'rb'))

        for lon, lat in notnull_coords:
            composite_grid.loc[lat, lon] = da_merge[varname].sel(Set=key, lat=lat, lon=lon)

    composite_grid = composite_grid.expand_dims(Set = ['No_rot_Composite'])
    
    return composite_grid

#----------------------------------------------------------
def create_composite_grid_monthly(da_merge, varname):
    """Create a composite grid by merging certain regions from each set
    :param: da_merge:      xarray
    :param: varname:       variable of interest
    """

    lat    = da_merge.lat
    lon    = da_merge.lon
    month  = da_merge.month

    nlat   = len(lat.values)
    nlon   = len(lon.values)
    nmonth = len(month.values)

    # Create empty gridded array
    composite_grid = np.empty([nlat, nlon, nmonth])

    # Adding dimensions and coordinates
    composite_grid = xr.DataArray(composite_grid, dims=('lat', 'lon', 'month'))
    composite_grid = composite_grid.assign_coords(lat=lat.values, lon=lon.values, month=month.values)
    composite_grid.name = varname

    pickle_fname = '/qfs/people/sinh210/wrk/E3SM_SFA/ELM-Bioenergy/spatial_plots/figures/domain.lnd.Northern_Rockies_cruncep_c220216.out'

    # Dictionary for subregions
    myDict_region = {'Set1': 'Northern_Rockies',
                     'Set2': 'Upper_Midwest',
                     'Set3': 'Ohio_Valley'}

    #iterate through dictionary
    for i, key in enumerate(myDict_region):
    
        # load pickle to read lon_lat coordinates for three sets
        notnull_coords = pickle.load(open(pickle_fname.replace('Northern_Rockies', myDict_region[key]), 'rb'))

        for lon, lat in notnull_coords:
            composite_grid.loc[lat, lon] = da_merge[varname].sel(Set=key, lat=lat, lon=lon)

    composite_grid = composite_grid.expand_dims(Set = ['Composite'])
    
    return composite_grid

#----------------------------------------------------------
def create_no_rot_composite_grid_monthly(da_merge, varname):
    """Create a composite grid by merging certain regions from each set
    :param: da_merge:      xarray
    :param: varname:       variable of interest
    """

    lat    = da_merge.lat
    lon    = da_merge.lon
    month  = da_merge.month

    nlat   = len(lat.values)
    nlon   = len(lon.values)
    nmonth = len(month.values)

    # Create empty gridded array
    composite_grid = np.empty([nlat, nlon, nmonth])

    # Adding dimensions and coordinates
    composite_grid = xr.DataArray(composite_grid, dims=('lat', 'lon', 'month'))
    composite_grid = composite_grid.assign_coords(lat=lat.values, lon=lon.values, month=month.values)
    composite_grid.name = varname

    pickle_fname = '/qfs/people/sinh210/wrk/E3SM_SFA/ELM-Bioenergy/spatial_plots/figures/domain.lnd.Northern_Rockies_cruncep_c220216.out'

    # Dictionary for subregions
    myDict_region = {'Set1_no_rot': 'Northern_Rockies',
                     'Set2_no_rot': 'Upper_Midwest',
                     'Set3_no_rot': 'Ohio_Valley'}

    #iterate through dictionary
    for i, key in enumerate(myDict_region):
    
        # load pickle to read lon_lat coordinates for three sets
        notnull_coords = pickle.load(open(pickle_fname.replace('Northern_Rockies', myDict_region[key]), 'rb'))

        for lon, lat in notnull_coords:
            composite_grid.loc[lat, lon] = da_merge[varname].sel(Set=key, lat=lat, lon=lon)

    composite_grid = composite_grid.expand_dims(Set = ['No_rot_Composite'])
    
    return composite_grid

#----------------------------------------------------------
def create_regridded_composite_grid(da_merge, varname, plot_var):
    """Create a composite grid by merging certain regions from each set
    :param: da_merge:      xarray
    :param: varname:       variable of interest
    """

    pft  = da_merge[plot_var]
    lat  = da_merge.lat
    lon  = da_merge.lon

    npft = len(pft.values)
    nlat = len(lat.values)
    nlon = len(lon.values)

    # Create empty gridded array
    composite_grid = np.empty([npft, nlat, nlon])

    # Adding dimensions and coordinates
    composite_grid = xr.DataArray(composite_grid, dims=(plot_var, 'lat', 'lon'))
    if(plot_var == 'pft'):
       composite_grid = composite_grid.assign_coords(pft=pft.values, lat=lat.values, lon=lon.values)
    if(plot_var == 'col'):
       composite_grid = composite_grid.assign_coords(col=pft.values, lat=lat.values, lon=lon.values)
    composite_grid.name = varname

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
            composite_grid.loc[:, lat, lon] = da_merge[varname].sel(Set=key, lat=lat, lon=lon)

    composite_grid = composite_grid.expand_dims(Set = ['Composite'])
 
    return composite_grid
#----------------------------------------------------------

def create_no_rot_regridded_composite_grid(da_merge, varname, plot_var):
    """Create a composite grid by merging certain regions from each set
    :param: da_merge:      xarray
    :param: varname:       variable of interest
    """

    pft  = da_merge[plot_var]
    lat  = da_merge.lat
    lon  = da_merge.lon

    npft = len(pft.values)
    nlat = len(lat.values)
    nlon = len(lon.values)

    # Create empty gridded array
    composite_grid = np.empty([npft, nlat, nlon])

    # Adding dimensions and coordinates
    composite_grid = xr.DataArray(composite_grid, dims=(plot_var, 'lat', 'lon'))
    if(plot_var == 'pft'):
       composite_grid = composite_grid.assign_coords(pft=pft.values, lat=lat.values, lon=lon.values)
    if(plot_var == 'col'):
       composite_grid = composite_grid.assign_coords(col=pft.values, lat=lat.values, lon=lon.values)
    composite_grid.name = varname

    # Dictionary for subregions
    myDict_region = {'Set1_no_rot': 'Northern_Rockies',
                     'Set2_no_rot': 'Upper_Midwest',
                     'Set3_no_rot': 'Ohio_Valley'}

    pickle_fname = '/qfs/people/sinh210/wrk/E3SM_SFA/ELM-Bioenergy/spatial_plots/figures/domain.lnd.Northern_Rockies_cruncep_c220216.out'

    #iterate through dictionary
    for i, key in enumerate(myDict_region):
    
        # load pickle to read lon_lat coordinates for three sets
        notnull_coords = pickle.load(open(pickle_fname.replace('Northern_Rockies', myDict_region[key]), 'rb'))

        for lon, lat in notnull_coords:
            composite_grid.loc[:, lat, lon] = da_merge[varname].sel(Set=key, lat=lat, lon=lon)

    composite_grid = composite_grid.expand_dims(Set = ['No_rot_Composite'])
 
    return composite_grid
#----------------------------------------------------------
