#!/bin/bash

# ----- Load modules -----
module load anaconda2
source activate myenv
unset PYTHONHOME

# ----- Directory paths -----
export USERID=sinh210
export BASE_DIR=/qfs/people/${USERID}/wrk/E3SM_SFA
export E3SM_DIR=${BASE_DIR}/E3SM
export OLMT_DIR=${BASE_DIR}/OLMT
export CCSM_INPUT_DIR=/compyfs/inputdata
export REG_DATA_DIR=/compyfs/${USERID}/mygetregionaldata

# ------ Options for running OLMT -----
export RES=ELM_USRDAT
export SITE=US-Ne3
#export SITE=US-Ro1
#export SITE=US-UiC
#export SITE=default
export CASEID=20220711_20x34_corn_soy_rot_${SITE}_param
#export CASEID=20220609_20x34_${SITE}_param
export MACH=compy

# ----- Modified input file location -----
export MOD_PARM_FILE=${BASE_DIR}/E3SM_cases/paramdata/clm_params_${SITE}_c220328.nc

export DOMAIN_FILE=${REG_DATA_DIR}/domain.lnd.20x34pt_f19_US_Midwest_sub_cruncep_c220216.nc
export SURF_FILE=${REG_DATA_DIR}/surfdata_20x34pt_f19_US_Midwest_sub_cru_50pfts_simyr1850_c220216.nc
export LANDUSE_FILE=${REG_DATA_DIR}/landuse.timeseries_20x34pt_f19_US_Midwest_sub_cru_hist_50pfts_corn_soy_rot_c220216.nc
#export LANDUSE_FILE=${REG_DATA_DIR}/landuse.timeseries_20x34pt_f19_US_Midwest_sub_cru_hist_50pfts_c220413.nc

# ------ Run OLMT -----
cd ${OLMT_DIR}

# --mod_parm_file ${MOD_PARM_FILE} \
# modified parameter file not used for default run
# place the line below option for --landusefile for site specific parameter files
python ./global_fullrun.py \
 --caseidprefix ${CASEID} \
 --cpl_bypass \
 --gswp3 \
 --machine ${MACH} \
 --project e3sm \
 --ccsm_input ${CCSM_INPUT_DIR} \
 --model_root ${E3SM_DIR} \
 --domainfile ${DOMAIN_FILE} \
 --surffile ${SURF_FILE} \
 --landusefile ${LANDUSE_FILE} \
 --mod_parm_file ${MOD_PARM_FILE} \
 --res ${RES} \
 --crop \
 --nyears_ad_spinup 200 \
 --nyears_final_spinup 200 \
 --run_startyear 1 \
 --nyears_transient 165 \
 --hist_mfilt_trans 12 \
 --hist_nhtfrq_trans 0 \
 --tstep 1


# ----- Modify user_nl_elm for the transient case -----
cd ${E3SM_DIR}/cime/scripts/${CASEID}_${RES}_ICBELMCNCROP_trans

cat >> user_nl_elm << EOF
 hist_mfilt = 12, 12
 hist_nhtfrq = 0, 0
 hist_dov2xy = .true., .false.
 hist_fincl2 = 'GPP', 'ER', 'EFLX_LH_TOT', 'FSH', 'DMYIELD', 'TOTCOLC', 'TOTSOMC', 'TOTSOMN', 'TOTSOMP','PLANTDAY', 'HARVESTDAY', 'TLAI', 'LEAFC'
EOF

./case.setup
cd ${BASE_DIR}/E3SM_cases/scripts
