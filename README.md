_your zenodo badge here_

# Sinha\_etal\_2022\_JGR_Bio

**The Impact of Crop Rotation and Spatially Varying Crop Parameters in the E3SM Land Model (ELMv2)**

Eva Sinha<sup>1\*</sup>, Ben Bond-Lamberty<sup>2</sup>, Katherine V. Calvin<sup>2</sup>, Beth A. Drewniak<sup>3</sup>, Gautam Bisht<sup>1</sup>, Carl Bernacchi<sup>4,5</sup>, Bethany J. Blakely<sup>5</sup>, and Caitlin E. Moore<sup>5,6</sup>

<sup>1</sup>Pacific Northwest National Laboratory, Richland, WA, United States  
<sup>2</sup>Joint Global Change Research Institute, Pacific Northwest National Laboratory, College Park, MD, United States  
<sup>3</sup>Argonne National Laboratory, Lemont, IL, United States  
<sup>4</sup>Global Change and Photosynthesis Research Unit, USDA-ARS, Urbana, IL, United States  
<sup>5</sup>University of Illinois at Urbana‐Champaign, Urbana, IL, United States  
<sup>6</sup>School of Agriculture and Environment, The University of Western Australia, Crawley, WA, Australia

\* corresponding author:  eva.sinha@pnnl.gov

## Abstract
Earth System Models (ESMs) are increasingly representing agriculture due to its impact on biogeochemical cycles, local and regional climate, and fundamental importance for human society.
Realistic large scale simulations may require spatially varying crop parameters, that capture crop growth at various scales and among different cultivars, and common crop management practices, but their importance is uncertain, and they are often not represented in ESMs. 
In this study, we examine the impact of using constant vs. spatially varying crop parameters on a novel, realistic crop rotation scenario in the Energy Exascale Earth System Model (E3SM) Land Model version 2 (ELMv2).
We implemented crop rotation by using ELMv2's dynamic land unit capability, and then calibrated and validated the model against observations collected at three AmeriFlux sites in the US Midwest with corn soybean rotation.
The calibrated model closely captured the magnitude and observed seasonality of carbon and energy fluxes across crops and sites. 
We performed regional simulations for the US Midwest using the calibrated model and found that spatially varying only few crop parameters across the region, as opposed to using constant parameters, had a large impact, with the carbon fluxes varying by up to 40\% and energy fluxes by up to 30\%. 
These results imply that large scale ESM simulations using spatially invariant crop parameters may result in biased energy and carbon fluxes estimation from agricultural land, and underline the importance of improving human-earth systems interactions in ESMs.

## Journal reference
Sinha, E., Bond-Lamberty B., Calvin, K.V., Bisht, G., Drewniak, B., Bernacchi, C., Blakely, B., Moore, C., 2022. The Impact of Crop Rotation and Spatially Varying Crop Parameters in the E3SM Land Model (ELMv2). (In progress) JGR Biogeosciences, Submitted

## Code reference
Sinha, E., Bond-Lamberty B., Calvin, K.V., Bisht, G., Drewniak, B., Bernacchi, C., Blakely, B., Moore, C., 2022. Supporting code for Sinha et al. 2022 - TBD [Code]. Zenodo. http://doi.org/some-doi-number/zenodo.7777777

## Data reference

### Input data
Reference for each minted data source for your input data.  For example:

1. Andy Suyker (2022), AmeriFlux BASE US-Ne3 Mead - rainfed maize-soybean rotation site, Ver. 12-5, AmeriFlux AMP, (Dataset). https://doi.org/10.17190/AMF/1246086.
2. John Baker, Tim Griffis, Timothy Griffis (2018), AmeriFlux BASE US-Ro1 Rosemount- G21, Ver. 5-5, AmeriFlux AMP, (Dataset). https://doi.org/10.17190/AMF/1246092.
3. Carl J Bernacchi (2022), AmeriFlux BASE US-UiC University of Illinois Maize-Soy, Ver. 1-5, AmeriFlux AMP, (Dataset). https://doi.org/10.17190/AMF/1846665.
4. Hurtt, G. C., Chini, L., Sahajpal, R., Frolking, S., Bodirsky, B. L., Calvin, K., Doelman, J. C., Fisk, J., Fujimori, S., Klein Goldewijk, K., et al.: Harmonization of global land use change and management for the period 850–2100 (LUH2) for CMIP6, Geoscientific Model Development, 13, 5425–5464, 2020. https://doi.org/10.5194/gmd-2019-360.


### Output data
Sinha, E., Bond-Lamberty B., Calvin, K.V., Bisht, G., Drewniak, B., Bernacchi, C., Blakely, B., Moore, C., 2022. Supporting data for Sinha et al. 2022 - TBD [Code]. Zenodo. http://doi.org/some-doi-number/zenodo.7777777

## Contributing modeling software
| Model | Version | Repository Link | DOI |
|-------|---------|-----------------|-----|
| E3SM | version | https://github.com/E3SM-Project/E3SM | link to DOI dataset |

## Reproduce my experiment

1. Clone and install [E3SM](https://github.com/E3SM-Project/E3SM).

## Reproduce my figures
Use the following scripts found in the `workflow` directory to reproduce the figures used in this publication.

| Script Name | Description | How to Run |
| --- | --- | --- |
| `plot_site_loc.py` | Makes spatial plots showing Ameriflux site locations and three sub-regions of US-Midwest used for the regional run| `python plot_site_loc.py` |
| `run_site_calib_outputs.sh` | Makes plots of sensitivity analysis and model calibration for all three calibration sites |`./run_site_calib_outputs.sh` |
| `create_landuse_ts_corn_soy_rot.py` | Create land use timeseries for corn soybean rotation and make spatial plot of corn soybean CFT fraction and grid cells with corn soybean rotation | `python create_landuse_ts_corn_soy_rot.py`|
| `plot_ELM_output.py` | Makes spatial plots comparing impact of constant vs. varying parameters | `python plot_ELM_output.py` |
| `merge_images.py` | Merge images to produce final plot | `python merge_images.py` |
| `pft_regridding.py` | Read ELM h1 output in 2D vector format [time, pft] and convert to 4D vector format [time, pft, lat, lon] | `python pft_regridding.py` |
| `plot_ELM_pft_regridded.py` | Makes spatial plots comparing impact of constant vs. varying parameters at pft level | `python plot_ELM_pft_regridded.py`|
| `plot_annual_site_model_obs.py` | Make bar plot comparing annual simulated vs observed fluxes at AmeriFlux sites | `python plot_annual_site_model_obs.py`|
| `plot_monthly_site_model_obs.py` | Make line plot comparing monthly simulated vs observed fluxes at AmeriFlux sites | `python plot_monthly_site_model_obs.py`|

## Figures

### Site-scale calibration & validation
1. [Sensitivity analysis plot for US-Ne3](figures/fig_SA_US-Ne3.png)
2. [Sensitivity analysis plot for US-Ro1](figures/fig_SA_US-Ro1.png)
3. [Sensitivity analysis plot for US-UiC](figures/fig_SA_US-UiC.png)
4. [Model calibration comparing observed vs. modeled fluxes for US-Ne3](figures/fig_US-Ne3_calibration.png)
5. [Model calibration comparing observed vs. modeled fluxes for US-Ro1](figures/fig_US-Ro1_calibration.png)
6. [Model calibration comparing observed vs. modeled fluxes for US-UiC](figures/fig_US-UiC_calibration.png)
4. [Model validation comparing observed vs. modeled fluxes for US-Ne3](figures/fig_US-Ne3_validation.png)
5. [Model validation comparing observed vs. modeled fluxes for US-Ro1](figures/fig_US-Ro1_validation.png)
6. [Model validation comparing observed vs. modeled fluxes for US-UiC](figures/fig_US-UiC_validation.png)
7. [Model validation comparing observed vs. modeled LAI for US-Ne3](figures/fig_US-Ne3_LAI.png)
8. [Model validation comparing observed vs. modeled LAI for US-Ro1](figures/fig_US-Ro1_LAI.png)
9. [Model validation comparing observed vs. modeled LAI for US-UiC](figures/fig_US-UiC_LAI.png)
10. [Model validation comparing observed vs. modeled harvest for US-Ne3](figures/fig_US-Ne3_harvest.png)
11. [Model validation comparing observed vs. modeled harvest for US-Ro1](figures/fig_US-Ro1_harvest.png)
12. [Model validation comparing observed vs. modeled harvest for US-UiC](figures/fig_US-UiC_harvest.png)
13. [Impact of crop rotation on annual GPP](figures/20220328_corn_soybean_US-Ne3_corn_annual_GPP.png)

### Regional analysis
1. [Ameriflux site locations and three sub-regions](figures/fig_Regions.png)
2. [Percent of corn and soybean crop functional type and fraction of grid cells with corn soybean rotation](figures/fig_regional_corn_soybean_cft_rotation.png)
3. [Impact of constant vs. varying parameters on annual GPP](figures/fig_regional_Annual_GPP.png)
4. [Impact of constant vs. varying parameters on annual ER](figures/fig_regional_Annual_ER.png)
5. [Impact of constant vs. varying parameters on latent heat flux for summer](figures/fig_regional_Summer_months_LE.png)
6. [Impact of constant vs. varying parameters on sensible heat flux for summer](figures/fig_regional_Summer_months_H.png)
7. [Comparing simulated annual GPP to FluxCom estimates](figures/fig_regional_GPP_Model_vs_FluxCom.png)
8. [Comparing simulated annual GPP to Madani and Parazoo (2020) estimates](figures/fig_regional_GPP_Model_vs_Madani_et_al.png)
9. [Impact of constant vs. varying parameters on annual GPP at pft level](figures/fig_regional_Annual_GPP_cft.png)
10. [Comparison of simulated and observed annual GPP at AmeriFlux calibration/validation sites](figures/Sitelevel_Annual_GPP_pft.png)
11. [Comparison of simulated and observed monthly GPP at AmeriFlux calibration/validation sites](figures/Sitelevel_GPP_pft_lineplot.png)
12. [Comparison of simulated and observed monthly latent heat flux at AmeriFlux calibration/validation sites](figures/Sitelevel_EFLX_LH_TOT_pft_lineplot.png)
