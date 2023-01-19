import xarray as xr

from util_estimate_dataset_stats import *

# -----------------------------------------------------------
def read_model_output(yr_start, yr_end, fpath, caseid, varnames):
    """Read ELM model output for select variables
        param: yr_start      start year for reading model output
        param: yr_end        end year for reading model output
        param: fpath         directory path
        param: caseid        model run case id
        param: varnames      variable name for subsetting
        :return:             data array with model output
        """

    # Read names of all NetCDF files within the given year range
    fnames = []
    for yr in range(int(yr_start), int(yr_end)+1):
        fnames.append(fpath + '/' + caseid + '.elm.h0.' + str(yr) + '-02-01-00000.nc')

    # Open a multiple netCDF data file and load the data into xarrays
    with xr.open_mfdataset(fnames, combine='nested', concat_dim='time') as ds:

        # Only keep select variables in the data array
        ds = ds[varnames]

    return(ds)

# -----------------------------------------------------------
def read_spinup_model_output(yr_start, yr_end, yr_step, fpath, caseid, mon_day_str, varnames, decode_times=True):
    """Read ELM model output for select variables
        param: yr_start      start year for reading model output
        param: yr_end        end year for reading model output
        param: fpath         directory path
        param: caseid        model run case id
        param: varnames      variable name for subsetting
        :return:             data array with model output
        """

    # Read names of all NetCDF files within the given year range
    fnames = []
    for yr in range(int(yr_start), int(yr_end)+1, yr_step):
        fnames.append(fpath + '/' + caseid + '.elm.h0.' + str(yr).zfill(4) + mon_day_str + '-00000.nc')

    # Open a multiple netCDF data file and load the data into xarrays
    with xr.open_mfdataset(fnames, decode_times=decode_times, combine='nested', concat_dim='time', data_vars='minimal') as ds:

        # Only keep select variables in the data array
        ds = ds[varnames]

    return(ds)

# -----------------------------------------------------------
def read_col_lev_model_output(yr_start, yr_end, filepath, caseid):
    """Read ELM model output for select variables
    :param: yr_start     start year for reading model output
    :param: yr_end       end year for reading model output
    :param: filepath     directory path
    :param: caseid       model run case id
    :return:             data array with model output
    """

    # Read names of all NetCDF files within the given year range
    fnames = []
    for yr in range(int(yr_start), int(yr_end)+1):
        fnames.append(filepath + '/' + caseid + '.elm.h1.' + str(yr) + '-02-01-00000.nc')

    # Open a multiple netCDF data file and load the data into xarray
    ds = xr.open_mfdataset(fnames, combine='nested', concat_dim='time')

    return(ds)

# -----------------------------------------------------------
def read_FluxCom_data(yr_start, yr_end, fpath, fname, varname):
    """Read ELM model output for select variables
        param: yr_start      start year for reading model output
        param: yr_end        end year for reading model output
        param: fpath         directory path
        param: caseid        model run case id
        param: varnames      variable name for subsetting
        :return:             data array with model output
        """
    # Read names of all NetCDF files within the given year range
    fnames = []
    for yr in range(int(yr_start), int(yr_end)+1):
        fnames.append(fpath + varname + fname + str(yr) + '.nc')

    # Open a multiple netCDF data file and load the data into xarrays
    with xr.open_mfdataset(fnames, combine='nested', concat_dim='time') as ds: 

        # Only keep select variables in the data array
        ds = ds[varname]

    return ds

#----------------------------------------------------------
def read_MODIS_monthly_data(fpath, fname):

   # Read names of all NetCDF files within the given year range
   fnames = []
   for ind in range(1, 13):
      fnames.append(fpath + fname + str(ind) +'.nc')

   # Open a multiple netCDF data file and load the data into xarrays
   ds = xr.open_mfdataset(fnames, combine='nested', concat_dim='month')

   return ds

# -----------------------------------------------------------
# Read site level observations
def read_site_level_obs(site, crop, var, conv_factor, time_period, est_mon_total, select_month='August'):

   basedir = '/qfs/people/sinh210/wrk/E3SM_SFA/ELM-Bioenergy/timeseries_plots/' 
   obsdir  = basedir + site + '_' + crop + '/' 
   obsfname = site + '_' + crop + '_select_var.nc'

   # Open a netcdf containing observed data
   ds_obs = xr.open_dataset(obsdir + obsfname)

   # Observations are at daily time scale
   # Therefore just adding data for all days in the year will provide annual total
   if(time_period == 'Annual'):
      da_plot = create_mean_annual_da(ds_obs[var], var, conv_factor, est_mon_total).values
   elif(time_period == 'Monthly'):
      da_plot = create_summer_average_monthly(ds_obs[var], all_mon, all_mon_str, var, conv_factor, est_mon_total)

      # Only keep data for a select month
      da_plot = da_plot.sel(month = select_month).values

   return(da_plot)

