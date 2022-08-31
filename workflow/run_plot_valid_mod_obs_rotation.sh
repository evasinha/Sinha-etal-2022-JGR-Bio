#!/bin/bash

export CASE_PRE=20220328_corn_soybean

# ----- Directory paths -----
export RUN_DIR_PATH=/lcrc/group/acme/ac.eva.sinha

for SITE in 'US-Ne3' 'US-Ro1' 'US-UiC'
do
   for CROP in 'corn' 'soybean'
   do
      export CASEID=${CASE_PRE}_${SITE}_ICBELMCNCROP_trans
      export RUN_DIR=${RUN_DIR_PATH}/${CASEID}/run
      export OBSDIR=${SITE}_${CROP}/
      export OBSFNAME=${SITE}_${CROP}_select_var.nc
      export FNAMEPRE=${CASE_PRE}_${SITE}

      python plot_valid_mod_obs_rotation.py --site ${SITE} --crop ${CROP} --rundir ${RUN_DIR} --caseid ${CASEID} --obsdir ${OBSDIR} --obsfname ${OBSFNAME}  --fnamepre ${FNAMEPRE}_${CROP}

      export OBSFNAME=${SITE}_all_yrs_select_var.nc
      python plot_mod_obs_all_yrs.py --site ${SITE} --rundir ${RUN_DIR} --caseid ${CASEID} --obsdir ${OBSDIR} --obsfname ${OBSFNAME}  --fnamepre ${FNAMEPRE}_${CROP}

   done
done
