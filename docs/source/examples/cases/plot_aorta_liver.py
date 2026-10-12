"""
===============
Aorta and Liver
===============

These example shows the use of the `~dcmri.AortaLiver` model to 
fit signals measured in aorta and liver simultaneously. 

"""

import numpy as np
import pydmr
import dcmri as dc


# %%
# Model setup
# -----------
# Since we are using data from the `TRISTAN healthy volunteer study with 
# rifampicin <https://zenodo.org/records/20210596>`_, we'll configure 
# the model with the following options:

aol = dc.InverseAortaLiver(
    heartlung='pfcomp',         # Smoother first pass data
    organs='2cxm',              # Long acquisition times reveal extravasation
    liver='1I-IC',              # Intracellular agent
    baseline='measured',        # Data are available on precontrast T1
    sequence='ZTE-3D-SPGR-SS',  # Echo times are assumed to be zero
    t2s_relaxation_ao=None,     # No T2* relaxation with TE=0
    t2s_relaxation_li=None,     # No T2* relaxation with TE=0
    calibrate=True,             # Derive signal scaling factor from data
)

# %%
# Let's see what input parameters are needed for this model:

aol.print_inputs()

# %%
# Since we want to analyse multiple datasets, we'll first define a helper 
# function which returns a dictionary with required data. 

def get_data(study, participant, visit): 

    # --- Load the data
    file = dc.fetch(study)
    data = pydmr.read(file, 'nest')

    # --- Get the subject-level data
    roi = data['rois'][participant][visit]
    par = data['pars'][participant][visit]

    # --- Get GFR from screening visit if available
    if 'eGFR_abs' in data['pars'][participant]['screening']:
        eGFR = data['pars'][participant]['screening']['eGFR_abs']
    else:
        eGFR = data['pars'][participant][visit]['eGFR_abs']

  # --- Time arrays
    time = [
        roi['time_1'] - roi['time_1'][0],
    ]

    data = {     

        # Electromagnetic
        'R1_b': 1 / par['T1_aorta_1'], 
        'R1_li': 1 / par['T1_liver_1'],

        # Hyperparameter
        'dt': 0.5,

        # Indicator
        'agent': 'gadoxetate',
        'BAT': dc.estimate_bat(time[0], roi['aorta_1']),

        # Physiological
        'GFR': eGFR / 60,

        # Sequence
        'FA': par['FA_1'],
        'field_strength': 3,
        'Nk0': int(np.round(time[0][1] / par['TR'] / 2)),
        'Nph': int(np.round(time[0][1] / par['TR'])),
        'TR': par['TR'],

        # Whole body
        'vol_li': par['liver_volume'],
        'weight': par['weight'], 
    }

    scan = 1
    # Indicator group
    data[f'rate'] = 1
    data[f'dose'] = par[f'dose_{scan}']

    # Signal group
    data[f'nb'] = int(par['t0'] / (time[0][1] - time[0][0]))
    for r in ['aorta', 'liver']:
        data[f'tS_{r[:2]}'] = time[0]
        data[f'S_{r[:2]}'] = roi[f'{r}_{scan}']
        data[f'iStrig_{r[:2]}'] = roi[f'{r}_{scan}']

    return data


# %%
# Fitting the model
# -----------------
study = 'tristan_humans_healthy_rifampicin'

# --- Format the data
visit_1_data = get_data(study, 'LDS-002', 'control')
visit_2_data = get_data(study, 'LDS-002', 'drug')

# --- Fit the models
visit_1_result = aol(visit_1_data, verbose=0)
visit_2_result = aol(visit_2_data, verbose=0)

# %%
# Before we interpret the results, let's verify the optimization has 
# converged to a solution:

# --- Update the data
visit_1_data |= visit_1_result['popt']
visit_2_data |= visit_2_result['popt']

# --- Plot the fits
aol.plot(visit_1_data)
aol.plot(visit_2_data)

# %%
# The model first the data well, so we can now consider the 
# values for the derived parameters
dc.print_quantities(visit_1_result['pder'], 'control', digits=2)
dc.print_quantities(visit_2_result['pder'], 'drug', digits=2)

# sphinx_gallery_start_ignore
# sphinx_gallery_thumbnail_number = -1
# sphinx_gallery_end_ignore
