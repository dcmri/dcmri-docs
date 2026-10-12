"""
============================
Aorta and Liver in two scans
============================

These example shows the use of the `~dcmri.AortaLiverSplit` model to 
simultaneously fit signals measured in aorta and liver over two 
different scans on the same day. 
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

model = dc.InverseAortaLiverSplit(
    heartlung='pfcomp',         # Smoother first pass data
    organs='2cxm',              # Long acquisition times reveal extravasation
    liver='1I-IC',              # Intracellular agent
    non_stationary='U',         # Uptake rate changes during the course of the experiment
    baseline='measured',        # Data are available on precontrast T1
    sequence='ZTE-3D-SPGR-SS',  # Echo times are assumed to be zero
    t2s_relaxation_ao=None,     # No T2* relaxation with TE=0
    t2s_relaxation_li=None,     # No T2* relaxation with TE=0
    calibrate=True,             # Derive signal scaling factor from data
    trigger=True,               # Signals are retrospectively triggered
    bolus='dual',               # Two independent injections performed
)

# %%
# Let's see what input parameters are needed for this model:

model.print_inputs()

# %%
# For clarity and reusability we'll first define a helper 
# function which returns a dictionary with required data for a single 
# study participant and visit:

def get_data(study, participant, visit): 

    # --- Load the data
    file = dc.fetch(study)
    data = pydmr.read(file, 'nest')

    # --- Get the subject-level data
    roi = data['rois'][participant][visit]
    par = data['pars'][participant][visit]
    
    # --- Get GFR from screening visit if available
    par_screen = data['pars'][participant]['screening']
    eGFR = par_screen['eGFR_abs'] if 'eGFR_abs' in par_screen else par['eGFR_abs']

    # --- Time arrays
    time_1 = roi['time_1'] - roi['time_1'][0]
    time_2 = roi['time_2'] - roi['time_1'][0]

    return {     

        # Electromagnetic
        'R1_b': 1 / par['T1_aorta_1'], 
        'R1_li': 1 / par['T1_liver_1'], 

        # Hyperparameter
        'dt': 0.5,

        # Indicator
        'agent': 'gadoxetate',
        'BAT_1': dc.estimate_bat(time_1, roi['aorta_1'] ),
        'BAT_2': time_2[np.argmax(roi['aorta_2'])],
        'dose_1': par['dose_1'],
        'dose_2': par['dose_2'],
        'rate_1': 1,
        'rate_2': 1,

        # Physiological
        'GFR': eGFR / 60,

        # Sequence
        'FA': par['FA_1'],
        'field_strength': 3,
        'Nk0': int(np.round(time_1[1] / par['TR'] / 2)),
        'Nph': int(np.round(time_1[1] / par['TR'])),
        'TR': par['TR'],

        # Signal
        'iStrig_1_ao': roi['aorta_1_accept'],
        'iStrig_1_li': roi['liver_1_accept'],
        'iStrig_2_ao': roi['aorta_2_accept'],
        'iStrig_2_li': roi['liver_2_accept'],

        'nb_1': int(par['t0'] / (time_1[1] - time_1[0])),
        'nb_2': int(par['t0'] / (time_2[1] - time_2[0])),

        'S_1_ao': roi['aorta_1'] , 
        'S_2_ao': roi['aorta_2'],
        'S_1_li': roi['liver_1'], 
        'S_2_li': roi['liver_2'],

        'tS_1_ao': time_1,
        'tS_2_ao': time_2,
        'tS_1_li': time_1,
        'tS_2_li': time_2,

        # Whole body
        'vol_li': par['liver_volume'],
        'weight': par['weight'], 
    }

# %%
# Fitting the model
# -----------------

# --- Source data identifier
study = 'tristan_humans_healthy_rifampicin'

# --- Format the data
visit_1_data = get_data(study, 'LDS-002', 'control')
visit_2_data = get_data(study, 'LDS-002', 'drug')

# --- Fit the model
visit_1_result = model(visit_1_data, verbose=2)
visit_2_result = model(visit_2_data, verbose=2)

# %%
# Verify that the optimization has converged to a solution:

# --- Update the data
visit_1_data |= visit_1_result['popt'] 
visit_2_data |= visit_2_result['popt']

# --- Plot the fits
model.plot(visit_1_data)
model.plot(visit_2_data)

# %%
# The model first the data well, so we can now consider the 
# values for the derived parameters
dc.print_quantities(visit_1_result['pder'], 'Control visit', digits=2)
dc.print_quantities(visit_2_result['pder'], 'Drug visit', digits=2)

# sphinx_gallery_start_ignore
# sphinx_gallery_thumbnail_number = -1
# sphinx_gallery_end_ignore
