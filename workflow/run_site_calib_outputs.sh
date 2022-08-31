#!/bin/bash

for SITE in 'US-Ne3' 'US-Ro1' 'US-UiC'
do
   for CROP in 'Corn' 'Soybean'
   do
      python subplots_sens.py --site ${SITE} --crop ${CROP}
   done
done
