import os
import geopandas
import xarray as xr
#import xagg as xa
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from mapclassify import UserDefined

__author__ = 'Eva Sinha'
__email__  = 'eva.sinha@pnnl.gov'

from util_myDict_labels import *

# https://towardsdatascience.com/lets-make-a-map-using-geopandas-pandas-and-matplotlib-to-make-a-chloropleth-map-dddc31c1983d
# https://stackoverflow.com/questions/55107411/how-to-add-a-colorbar-to-geopandas-plot-with-matplotlib-animation
# https://github.com/geopandas/geopandas/issues/1019

#----------------------------------------------------------
def read_USDA_NASS_yield(fpath, fname, conv_factor, col_name):
    """Plot timeseries from input xarray
    :param: fpath:         path to input netcdf file for plotting

    """
    
    # ----- Read USDA_NASS yield data -----
    USDA_yield = pd.read_csv(fpath + fname)

    # Drop 'County ANSI' columns NaN rows
    USDA_yield = USDA_yield.dropna(subset=['County ANSI'])

    # Convert 'County ANSI column to integer
    USDA_yield['County ANSI'] = USDA_yield['County ANSI'].astype(int)

    # Add 0 in front to make string with width 3
    USDA_yield['County ANSI'] = USDA_yield['County ANSI'].astype(str).str.zfill(3)

    # Add new column for GEOID
    USDA_yield['GEOID'] = USDA_yield['State ANSI'].astype(str) + USDA_yield['County ANSI']

    # Subset yield data to only contain select columns
    USDA_yield_select = USDA_yield[['Year', 'Commodity', 'Data Item', 'Value', 'GEOID']]

    # Mean yield between 2000 and 2015
    USDA_yield_select = USDA_yield_select.groupby(['GEOID']).agg(Value = ('Value', np.mean))

    # Estimate yield in ton/ha
    USDA_yield_select[col_name] = USDA_yield_select['Value'] * conv_factor
    
    # Drop yield in bushel/acre
    USDA_yield_select.drop('Value', axis=1, inplace=True)
    
    return USDA_yield_select

#----------------------------------------------------------
def merge_county_shp_USDA_yield(fpath, corn_yield, soy_yield):

    # ----- Load county shapefile -----
    geo_county = geopandas.read_file(fpath + 'cb_2018_us_county_20m/cb_2018_us_county_20m.shp')

    # Merge county shapefile and corn and soybean yield
    geo_county = geo_county.merge(corn_yield, left_on='GEOID', right_on='GEOID')
    geo_county = geo_county.merge(soy_yield,  left_on='GEOID', right_on='GEOID')

    return geo_county

#----------------------------------------------------------
def plot_geo_data(geo_data, leg_label, fpath, fname):

    parameters = {'figure.titlesize':15,
                  'legend.fontsize': 12,
                  'legend.title_fontsize': 12,
                  'axes.labelsize' : 15,
                  'axes.titlesize' : 15,
                  'xtick.labelsize': 15,
                  'ytick.labelsize': 15,
                  'font.size'      : 15}
    
    plt.rcParams.update(parameters)

    # Change directory    
    os.chdir('../figures/')

    fig, ax = plt.subplots(nrows=1, ncols=2, sharex=True, sharey=False, 
                           figsize=(17, 10), constrained_layout=True)

    # https://github.com/geopandas/geopandas/issues/1019
    # define your bins
    usr_bins = [0,2,4,6,8,10,12,14,16]

    # Plot crop yield
    geo_data.plot(ax          = ax[0], 
                  column      = 'Corn_ton_ha',
                  cmap        = 'rainbow', 
                  edgecolor   = None,
                  scheme      = 'userdefined', 
                  classification_kwds={'bins':usr_bins},
                  legend      = False)
    
    geo_data.plot(ax          = ax[1], 
                  column      = 'Soy_ton_ha',
                  cmap        = 'rainbow', 
                  edgecolor   = None,
                  scheme      = 'userdefined', 
                  classification_kwds={'bins':usr_bins},
                  legend      = True,
                  legend_kwds = {'loc':           'center left', 
                                 'bbox_to_anchor':(0.8,0.25),
                                 'fmt':           '{:.0f}',
                                 'interval':      True,
                                 'title':         'Yield [ton/ha]'})

    # ----- Load states shapefile -----
    geo_states = geopandas.read_file(fpath + 'cb_2018_us_state_20m/cb_2018_us_state_20m.shp')

    # Add states boundary layer
    geo_states.geometry.boundary.plot(ax=ax[0], color=None, edgecolor='grey')
    geo_states.geometry.boundary.plot(ax=ax[1], color=None, edgecolor='grey')

    ax[0].set_title('Corn')
    ax[1].set_title('Soybean')
#     ax[0].annotate('Source: USDA_NASS',
#                 xy                  = (0.05, 0.15),  
#                 xycoords            = 'figure fraction', 
#                 horizontalalignment = 'left', 
#                 verticalalignment   = 'top', 
#                 fontsize            = 20, 
#                 color               = '#555555')
    
    for ax in ax.flat:
        ax.set_xlim(-125,-65)
        ax.set_ylim(25,50)
        ax.set_axis_off()
    
    plt.savefig(fname, bbox_inches='tight') 

    # Change directory    
    os.chdir('../workflow/')

#----------------------------------------------------------
def plot_obs_model_yield(da_plot, geo_county):

   # Subset county data to keep data only for select states
   # Illinois IL 17; Indiana IN 18; Iowa IA 19; 
   # Kansas KS 20; Kentucky KY 21;
   # Michigan MI 26; Minnesota MN 27; Missouri MO 29; 
   # Nebraska NE 31; North Dakota ND 38; Ohio OH 39;
   # South Dakota SD 46; Wisconsin WI 55; 
   midwest_county = geo_county[geo_county.STATEFP.isin(['17','18','19','20','21','26','27','29','31','38','39','46','55'])]
   iowa_county    = geo_county[geo_county.STATEFP.isin(['19'])]

   # Get overlap between pixels and polygons
   weightmap = xa.pixel_overlaps(da_plot, iowa_county, subset_bbox=True)

   # Aggregate data in [da_model] onto polygons
   aggregated = xa.aggregate(da_plot, weightmap)

   # Export as a dataframe
   aggregated.to_dataframe('agg_plot_data')
   print(agg_plot_data)

#----------------------------------------------------------

corn_yield        = read_USDA_NASS_yield(USDA_NASS_fpath, USDA_NASS_corn_fname, USDA_NASS_corn_conv_factor, col_name='Corn_ton_ha')
soy_yield         = read_USDA_NASS_yield(USDA_NASS_fpath, USDA_NASS_soy_fname,  USDA_NASS_soy_conv_factor,  col_name='Soy_ton_ha')

geo_county =  merge_county_shp_USDA_yield(USDA_NASS_fpath, corn_yield, soy_yield)

outfname   = 'USDA_NASS_corn_soybean_yield.pdf'
leg_label  = 'Average yield [ton/ha]'

plot_geo_data(geo_county, leg_label, USDA_NASS_fpath, outfname)

