"""
=====
Liver
=====

This example illustrates the use of `~dcmri.Liver` for fitting of signals 
measured in liver. 

This example illustrates the use of dcmri with a single case study, 
measuring liver function on Day 1 (control) and on Day 2 (after 
administration of an inhibitor drug). For a complete analysis of 
all data we refer to the 
`full pipeline <https://zenodo.org/records/15648009>`_.
"""

# %%
# Setup
# -----

# --- Import packages
import numpy as np
import pydmr
import dcmri as dc

# --- Fetch and read the data
dmrfile = dc.fetch('tristan_rats_healthy_six_drugs')
dmr = pydmr.read(dmrfile, 'nest')

# %%
# This study uses an intracellullar agent, and in rats the mixing in 
# the blood pool is fast, so we will use a single inlet model (1I). 
# All other default configurations are correct:
liver = dc.InverseLiver(
    kinetics='1I-IC-HF',
    calibrate=True,
)

# %%
# Let's see what input parameters are needed

liver.print_inputs()

# %%
# The measured input functions in this study are unstable 
# so we will analyse the data with a standardised input function.
# Since we will be running this on two different datasets, lets first 
# define a function which returns the data dictionary for a given 
# dataset:
def data_dict(subject, visit):

    # --- Get the data for the subject and visit
    roi = dmr['rois'][subject][visit]
    par = dmr['pars'][subject][visit]

    # --- Generate the input function 
    dt = 0.5
    bat = par['BAT'] + roi['time'][1] / 2
    t = np.arange(0, np.amax(roi['time']) + 180, dt)
    ca = dc.tristan_rat(t, BAT=bat, duration=par['duration'])

    # Acquisition is retrospectively triggered so Nph can be derived
    ts = roi['time'][1] - roi['time'][0]
    Nph = int(np.round(ts / par['TR'])) 

    # --- Create a data dictionary with values for all inputs
    return {
        'tS_li': roi['time'],
        'S_li': roi['liver'],
        'agent': 'gadoxetate',
        'ci_li': ca,
        'field_strength': par['field_strength'],
        'TR': par['TR'],
        'FA': par['FA'],
        'Nph': Nph, 
        'Nk0': int(np.round(Nph / 2)) ,
        'dt': dt,
        'nb': par['n0'],
        'F_p_li': 0.022,      # doi: 10.1021/acs.molpharmaceut.1c00206
        'H': 0.418,           # Cremer et al, J Cereb Blood Flow Metab 3, 254-256 (1983)
        'v_e_li': 0.23,
        'v_li': 1.0,
        'pfree': {'k_e2h':[0, 1], 'T_h': [0, 60 * 60]},
    }

# %%
# Now we are in a position to fit the data from both visits

# --- Fit the day 1 data
day_1_data = data_dict('S12-02', 'Day_1')
day_1_result = liver(day_1_data, verbose=2)

# --- Fit the day 2 data
day_2_data = data_dict('S12-02', 'Day_2')
day_2_result = liver(day_2_data, verbose=2)

# %%
# Before we interpret the results, let's verify the optimization has 
# converged to a solution:

# --- Update the data
day_1_data |= day_1_result['popt']
day_2_data |= day_2_result['popt']

# --- Plot the fits
liver.plot(day_1_data)
liver.plot(day_2_data)

# %%
# Print the values for the derived parameters
dc.print_quantities(day_1_result['popt'], 'Day 1', decimals=3)
dc.print_quantities(day_2_result['popt'], 'Day 2', decimals=3)

# # %%
# # The values confirm the effect of the drug on liver function. The 
# # liver extraction fraction of gadoxetate has dropped from 80% to 37% 
# # the hepatocellular uptake rate (khe) from 0.096 to 0.013 mL/sec/cm3, and 
# # the biliary excretion rate (kbh) from 0.0025 to 0.0013 mL/sec/cm3.

# sphinx_gallery_start_ignore
# Choose the last image as a thumbnail for the gallery
# sphinx_gallery_thumbnail_number = -1
# sphinx_gallery_end_ignore
