"""
Python modules for making spatial plots of ELM outputs
"""
import os
import sys 
from PIL import Image
import matplotlib as mpl 
mpl.use('Agg')

__author__ = 'Eva Sinha'
__email__  = 'eva.sinha@pnnl.gov'


# -----------------------------------------------------------
def merge_2images_horiz(im1, im2):
    w = im1.size[0] + im2.size[0]
    h = max(im1.size[1], im2.size[1])
    im = Image.new('RGBA', (w, h))

    im.paste(im1)
    im.paste(im2, (im1.size[0], 0))

    return im

# -----------------------------------------------------------
def merge_2images_vert(im1, im2):
    w = im1.size[0]
    h = im1.size[1] + im2.size[1]
    im = Image.new('RGBA', (w, h))

    im.paste(im1)
    im.paste(im2, ((im1.size[0] -  im2.size[0]), im1.size[1]))

    return im

# -----------------------------------------------------------
def merge_3images(im1, im2, im3):
    w = im1.size[0] + im2.size[0]
    h = max(im1.size[1], im2.size[1]) + im3.size[1] 
    im = Image.new('RGBA', (w, h))

    im.paste(im1)
    im.paste(im2, (im1.size[0], 0))
    im.paste(im3, (im1.size[0], max(im1.size[1], im2.size[1])))

    return im

# -----------------------------------------------------------
myDict_merge_3images = {'fig_regional_Annual_GPP.png': {'im1': 'fig_regional_Annual_GPP_Composite.png',
                                                        'im2': 'fig_regional_Annual_GPP_diff.png',
                                                        'im3': 'fig_regional_Annual_GPP_per_diff.png'},
                        'fig_regional_Annual_ER.png':  {'im1': 'fig_regional_Annual_ER_Composite.png',
                                                        'im2': 'fig_regional_Annual_ER_diff.png',
                                                        'im3': 'fig_regional_Annual_ER_per_diff.png'}}

myDict_merge_2images_vert = {'fig_regional_GPP_Model_vs_FluxCom.png':      {'im1': 'fig_regional_Annual_GPP_Model_vs_FluxCom_Default.png',
                                                                            'im2': 'fig_regional_Annual_GPP_Model_vs_FluxCom_Default_per_diff.png'},
                             'fig_regional_GPP_Model_vs_FluxCom_3sets.png': {'im1': 'fig_regional_Annual_GPP_Model_vs_FluxCom_3sets.png',
                                                                            'im2': 'fig_regional_Annual_GPP_Model_vs_FluxCom_3sets_per_diff.png'},
                             'fig_regional_GPP_Model_vs_Madani_et_al.png': {'im1': 'fig_regional_Annual_GPP_Model_vs_Madani_et_al_Default.png',
                                                                            'im2': 'fig_regional_Annual_GPP_Model_vs_Madani_et_al_Default_per_diff.png'},
                             'fig_regional_GPP_Model_vs_Madani_et_al_3sets.png': {'im1': 'fig_regional_Annual_GPP_Model_vs_Madani_et_al_3sets.png',
                                                                                  'im2': 'fig_regional_Annual_GPP_Model_vs_Madani_et_al_3sets_per_diff.png'}}
myDict_merge_2images_horiz = {'fig_SA_US-Ne3.png':                {'im1':'US-Ne3_Corn_sens_main_all.png',
                                                                   'im2':'US-Ne3_Soybean_sens_main_all.png'},
                              'fig_SA_US-Ro1.png':                {'im1':'US-Ro1_Corn_sens_main_all.png',
                                                                   'im2':'US-Ro1_Soybean_sens_main_all.png'},
                              'fig_SA_US-UiC.png':                {'im1':'US-UiC_Corn_sens_main_all.png',
                                                                   'im2':'US-UiC_Soybean_sens_main_all.png'},
                              'fig_SA_US-Ne3_NEW.png':            {'im1':'US-Ne3_Corn_sensbar_main_all.png',
                                                                   'im2':'US-Ne3_Soybean_sensbar_main_all.png'},
                              'fig_SA_US-Ro1_NEW.png':            {'im1':'US-Ro1_Corn_sensbar_main_all.png',
                                                                   'im2':'US-Ro1_Soybean_sensbar_main_all.png'},
                              'fig_SA_US-UiC_NEW.png':            {'im1':'US-UiC_Corn_sensbar_main_all.png',
                                                                   'im2':'US-UiC_Soybean_sensbar_main_all.png'},
                              'fig_US-Ne3_calibration.png':       {'im1':'US-Ne3_Corn_fit_shade.png',
                                                                   'im2':'US-Ne3_Soybean_fit_shade.png'},
                              'fig_US-Ro1_calibration.png':       {'im1':'US-Ro1_Corn_fit_shade.png',
                                                                   'im2':'US-Ro1_Soybean_fit_shade.png'},
                              'fig_US-UiC_calibration.png':       {'im1':'US-UiC_Corn_fit_shade.png',
                                                                   'im2':'US-UiC_Soybean_fit_shade.png'},
                              'fig_US-Ne3_validation.png':        {'im1':'20220328_corn_soybean_US-Ne3_corn_valid_model_obs.png',
                                                                   'im2':'20220328_corn_soybean_US-Ne3_soybean_valid_model_obs.png'},
                              'fig_US-Ro1_validation.png':        {'im1':'20220328_corn_soybean_US-Ro1_corn_valid_model_obs.png',
                                                                   'im2':'20220328_corn_soybean_US-Ro1_soybean_valid_model_obs.png'},
                              'fig_US-UiC_validation.png':        {'im1':'20220328_corn_soybean_US-UiC_corn_valid_model_obs.png',
                                                                   'im2':'20220328_corn_soybean_US-UiC_soybean_valid_model_obs.png'},
                              'fig_US-Ne3_LAI.png':               {'im1':'20220328_corn_soybean_US-Ne3_corn_valid_lai.png',
                                                                   'im2':'20220328_corn_soybean_US-Ne3_soybean_valid_lai.png'},
                              'fig_US-Ro1_LAI.png':               {'im1':'20220328_corn_soybean_US-Ro1_corn_valid_lai.png',
                                                                   'im2':'20220328_corn_soybean_US-Ro1_soybean_valid_lai.png'},
                              'fig_US-UiC_LAI.png':               {'im1':'20220328_corn_soybean_US-UiC_corn_valid_lai.png',
                                                                   'im2':'20220328_corn_soybean_US-UiC_soybean_valid_lai.png'},
                              'fig_US-Ne3_harvest.png':           {'im1':'20220328_corn_soybean_US-Ne3_corn_valid_harv.png',
                                                                   'im2':'20220328_corn_soybean_US-Ne3_soybean_valid_harv.png'},
                              'fig_US-Ro1_harvest.png':           {'im1':'20220328_corn_soybean_US-Ro1_corn_valid_harv.png',
                                                                   'im2':'20220328_corn_soybean_US-Ro1_soybean_valid_harv.png'},
                              'fig_US-UiC_harvest.png':           {'im1':'20220328_corn_soybean_US-UiC_corn_valid_harv.png',
                                                                   'im2':'20220328_corn_soybean_US-UiC_soybean_valid_harv.png'},
                              'fig_regional_Summer_months_LE.png':{'im1':'Summer_months_EFLX_LH_TOT_Composite.png',
                                                                   'im2':'Summer_months_EFLX_LH_TOT_per_diff.png'},
                              'fig_regional_Summer_months_H.png': {'im1':'Summer_months_FSH_Composite.png',
                                                                   'im2':'Summer_months_FSH_per_diff.png'},
                              'fig_regional_corn_soybean_cft_rotation.png': {'im1':'corn_soybean_cft_percent.png',
                                                                             'im2':'hist_trans_US_c4ann_to_c3nfx_gt_5per.png'},
                              'fig_regional_Annual_GPP_cft.png':  {'im1':'fig_regional_Annual_GPP_cft_Composite.png',
                                                                    'im2':'fig_regional_Annual_GPP_cft_diff.png'}}

fpath = '../figures/'

#iterate through dictionary
for i, key in enumerate(myDict_merge_3images):

   # Read images
   im1 = Image.open(fpath + myDict_merge_3images[key]['im1'])
   im2 = Image.open(fpath + myDict_merge_3images[key]['im2'])
   im3 = Image.open(fpath + myDict_merge_3images[key]['im3'])

   #print(im3.format, im3.size, im3.mode)

   new_image = merge_3images(im1, im2, im3)
   new_image.save('../figures/'+key,'png')

#iterate through dictionary
for i, key in enumerate(myDict_merge_2images_horiz):

   # Read images
   im1 = Image.open(fpath + myDict_merge_2images_horiz[key]['im1'])
   im2 = Image.open(fpath + myDict_merge_2images_horiz[key]['im2'])

   new_image = merge_2images_horiz(im1, im2)
   new_image.save('../figures/'+key,'png')

#iterate through dictionary
for i, key in enumerate(myDict_merge_2images_vert):

   # Read images
   im1 = Image.open(fpath + myDict_merge_2images_vert[key]['im1'])
   im2 = Image.open(fpath + myDict_merge_2images_vert[key]['im2'])

   new_image = merge_2images_vert(im1, im2)
   new_image.save('../figures/'+key,'png')
