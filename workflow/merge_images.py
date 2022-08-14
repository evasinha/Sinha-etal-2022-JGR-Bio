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
def merge_2images(im1, im2):
    w = im1.size[0] + im2.size[0]
    h = max(im1.size[1], im2.size[1])
    im = Image.new("RGBA", (w, h))

    im.paste(im1)
    im.paste(im2, (im1.size[0], 0))

    return im

# -----------------------------------------------------------
def merge_3images(im1, im2, im3):
    w = im1.size[0] + im2.size[0]
    h = max(im1.size[1], im2.size[1]) + im3.size[1] 
    im = Image.new("RGBA", (w, h))

    im.paste(im1)
    im.paste(im2, (im1.size[0], 0))
    im.paste(im3, (im1.size[0], max(im1.size[1], im2.size[1])))

    return im

# -----------------------------------------------------------
myDict_merge_images = {'fig_regional_Annual_GPP.png': {'im1': 'fig_regional_Annual_GPP_Composite.png',
                                                   'im2': 'fig_regional_Annual_GPP_diff.png',
                                                   'im3': 'fig_regional_Annual_GPP_per_diff.png'},
                       'fig_regional_Annual_ER.png':  {'im1': 'fig_regional_Annual_ER_Composite.png',
                                                   'im2': 'fig_regional_Annual_ER_diff.png',
                                                   'im3': 'fig_regional_Annual_ER_per_diff.png'}}

fpath = '../figures/'

#iterate through dictionary
for i, key in enumerate(myDict_merge_images):

   # Read images
   im1 = Image.open(fpath + myDict_merge_images[key]['im1'])
   im2 = Image.open(fpath + myDict_merge_images[key]['im2'])
   im3 = Image.open(fpath + myDict_merge_images[key]['im3'])

   print(im3.format, im3.size, im3.mode)

   new_image = merge_3images(im1, im2, im3)
   new_image.save('../figures/'+key,'png')
