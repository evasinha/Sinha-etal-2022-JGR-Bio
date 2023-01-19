# Dictionary for annual and monthly color bar labels
myDict_labels = {'Annual': {'GPP':'Gross Primary Productivity [$\mathregular{gC~m^{-2}~year^{-1}}$]',
                            'ER':'Ecosystem Respiration [$\mathregular{gC~m^{-2}~year^{-1}}$]', 
                             'EFLX_LH_TOT':'Latent Heat Flux [$\mathregular{W~m^{-2}}$]',
                             'FSH':'Sensible Heat Flux [$\mathregular{W~m^{-2}}$]',
                            'NEE':'Net Ecosystem Exchange [$\mathregular{gC~m^{-2}~year^{-1}}$]',
                            'NCEgCm2':'Net Carbon Exchange [$\mathregular{gC~m^{-2}~year^{-1}}$]',
                            'TER':'Terrestrial Ecosystem Respiration [$\mathregular{gC~m^{-2}~year^{-1}}$]',
                            'DMYIELD':'Annual Grain Yield [$\mathregular{t~ha^{-1}}$]',
                            'PLANTDAY':'Planting day',
                            'HARVESTDAY':'Harvest day',
                            'F_N2O_DENIT':'Denitrification N2O flux [$\mathregular{gN~m^{-2}~year^{-1}}$]',
                            'F_N2O_NIT':'Nitrification N2O flux [$\mathregular{gN~m^{-2}~year^{-1}}$]',
                            'TOTCOLC':'TOTCOLC [$\mathregular{gC~m^{-2}}$]',
                            'TOTSOMC':'TOTSOMC [$\mathregular{gC~m^{-2}}$]'},
                 'Monthly': {'GPP':'Gross Primary Productivity [$\mathregular{gC~m^{-2}~month^{-1}}$]',
                             'ER':'Ecosystem Respiration [$\mathregular{gC~m^{-2}~month^{-1}}$]',
                             'EFLX_LH_TOT':'Latent Heat Flux [$\mathregular{W~m^{-2}}$]',
                             'FSH':'Sensible Heat Flux [$\mathregular{W~m^{-2}}$]',
                             'TLAI':'Total projected leaf area index',
                             'LAI':'Leaf area index'}}

# Conversion constants
CONV_SEC_DAY = 1 / (24 * 60 * 60) 
CONV_umolCO2_gC = 1.03775

# Conversion factor for ELM model outputs
conv_factor = {'GPP':        CONV_SEC_DAY,
               'ER':         CONV_SEC_DAY,
               'NEE':        CONV_SEC_DAY,
               'NPP':        CONV_SEC_DAY,
               'NBP':        CONV_SEC_DAY,
               'TOTECOSYSC': 1,
               'TOTSOMC':    1,
               'EFLX_LH_TOT': 1,
               'FSH':         1,
               'TLAI':        1}

# Unit conversion factor for observations
obs_conv_factor = {'GPP':         1/CONV_umolCO2_gC,
                   'ER':          1/CONV_umolCO2_gC,
                   'EFLX_LH_TOT': 1}

# Dictionary for three cases
#myDict_caseid = {'Set1'        :'20220512_20x34_corn_soy_rot_US-Ne3_param_ELM_USRDAT_ICBELMCNCROP_trans',
#                 'Set2'        :'20220512_20x34_corn_soy_rot_US-Ro1_param_ELM_USRDAT_ICBELMCNCROP_trans',
#                 'Set3'        :'20220512_20x34_corn_soy_rot_US-UiC_param_ELM_USRDAT_ICBELMCNCROP_trans',
#                 'Default'     :'20220512_20x34_corn_soy_rot_default_param_ELM_USRDAT_ICBELMCNCROP_trans',
#                 'Set1_no_rot' :'20220609_20x34_US-Ne3_param_ELM_USRDAT_ICBELMCNCROP_trans',
#                 'Set2_no_rot' :'20220609_20x34_US-Ro1_param_ELM_USRDAT_ICBELMCNCROP_trans',
#                 'Set3_no_rot' :'20220609_20x34_US-UiC_param_ELM_USRDAT_ICBELMCNCROP_trans'}

myDict_caseid = {'Set1'        :'20230114_20x34_corn_soy_rot_US-Ne3_param_ELM_USRDAT_ICBELMCNCROP_trans',
                 'Set2'        :'20230114_20x34_corn_soy_rot_US-Ro1_param_ELM_USRDAT_ICBELMCNCROP_trans',
                 'Set3'        :'20230114_20x34_corn_soy_rot_US-UiC_param_ELM_USRDAT_ICBELMCNCROP_trans',
                 'Default'     :'20230114_20x34_corn_soy_rot_default_param_ELM_USRDAT_ICBELMCNCROP_trans',
                 'Set1_no_rot' :'20230114_20x34_US-Ne3_param_ELM_USRDAT_ICBELMCNCROP_trans',
                 'Set2_no_rot' :'20230114_20x34_US-Ro1_param_ELM_USRDAT_ICBELMCNCROP_trans',
                 'Set3_no_rot' :'20230114_20x34_US-UiC_param_ELM_USRDAT_ICBELMCNCROP_trans'}

sum_mon     = [6,7,8,9]
sum_mon_str = ['June', 'July', 'August', 'September']
select_month = 'August'
all_mon     = [1,2,3,4,5,6,7,8,9,10,11,12]
all_mon_str = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']

fig_extent  = [-99.5, -82, 36.75, 47.25]

yr_start = 2001
yr_end   = 2010

# ---------- FluxCom data ----------
FluxCom_METEO_ALL_fpath = '/qfs/people/sinh210/wrk/E3SM_SFA/ELM-Bioenergy/obsdata/FluxCom/CarbonFluxes/RS_METEO/ensemble/ALL/monthly/'

FluxCom_yr_start = 2001
FluxCom_yr_end   = 2010
FluxCom_METEO_ALL_var_fname  = {'GPP':'.RS_METEO.FP-ALL.MLM-ALL.METEO-ALL.720_360.monthly.',
                                'NEE':'.RS_METEO.FP-NONE.MLM-ALL.METEO-ALL.720_360.monthly.',
                                'TER':'.RS_METEO.FP-ALL.MLM-ALL.METEO-ALL.720_360.monthly.'} 

FluxCom_METEO_GSWP3_fpath = '/qfs/people/sinh210/wrk/E3SM_SFA/ELM-Bioenergy/obsdata/FluxCom/CarbonFluxes/RS_METEO/ensemble/GSWP3/monthly/'

FluxCom_METEO_GSWP3_var_fname  = {'GPP':'.RS_METEO.FP-ALL.MLM-ALL.METEO-GSWP3.720_360.monthly.',
                                  'NEE':'.RS_METEO.FP-NONE.MLM-ALL.METEO-GSWP3.720_360.monthly.',
                                  'TER':'.RS_METEO.FP-ALL.MLM-ALL.METEO-GSWP3.720_360.monthly.'} 

# ---------- Madani et al data ----------
Madani_et_al_fpath = '/qfs/people/sinh210/wrk/E3SM_SFA/ELM-Bioenergy/obsdata/daac.ornl.gov/daacdata/global_vegetation/Global_Monthly_GPP/data/'
Madani_et_al_fname = 'gross_primary_productivity_monthly_1982-2016_360x720.nc'

yang_saatchi_fpath = '/qfs/people/sinh210/wrk/E3SM_SFA/ELM-Bioenergy/obsdata/daac.ornl.gov/daacdata/cms/C_Pools_Fluxes_CONUS/data/'
yang_saatchi_fname = 'conus_GPP.nc4'

wolf_et_al_fpath = '/qfs/people/sinh210/wrk/E3SM_SFA/ELM-Bioenergy/obsdata/daac.ornl.gov/daacdata/cms/CMS_Global_Cropland_Carbon/data/'
wolf_et_al_fname = 'NCE_2005_2011_gCm2_360x720.nc'

MODIS_fpath = '/qfs/people/sinh210/wrk/E3SM_SFA/ELM-Bioenergy/obsdata/MODIS/'

# ---------- USDA_NASS data ----------
USDA_NASS_fpath  = '/qfs/people/sinh210/wrk/E3SM_SFA/ELM-Bioenergy/obsdata/USDA_NASS/'

# https://www.extension.iastate.edu/agdm/wholefarm/pdf/c6-80.pdf
# CORN    1 bushel/acre = .0628 (.06) metric tons/hectare
# SOYBEAN 1 bushel/acre = .0673 (.07) metric tons/hectare

USDA_NASS_corn_fname        = 'USDA-NASS_Corn_Yield_2000_2015.csv'
USDA_NASS_corn_conv_factor  = 0.0628

USDA_NASS_soy_fname         = 'USDA-NASS_Soybean_Yield_2000_2015.csv'
USDA_NASS_soy_conv_factor   = 0.0673
