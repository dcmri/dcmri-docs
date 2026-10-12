"""
============================
Inhibition of liver function
============================

These example shows the use of the `~dcmri.AortaLiverDrug` model to 
simultaneously fit signals measured in aorta and liver over two 
different visits. In the second visit, images are acquired after 
administering a drug that inhibits liver function. 

The joint modelling 
of these data allows us to exploit the fact that the majority of 
systemic parameters are not affected by the drug, and can therefore 
be assumed constant between both visits. 

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


model = dc.InverseAortaLiverDrug(
    heartlung='pfcomp',         # Smoother first pass data
    organs='2cxm',              # Long acquisition times reveal extravasation
    liver='1I-IC',              # Intracellular agent
    baseline='measured',        # Data are available on precontrast T1
    sequence='ZTE-3D-SPGR-SS',  # Echo times are assumed to be zero
    t2s_relaxation_ao=None,     # No T2* relaxation with TE=0
    t2s_relaxation_li=None,     # No T2* relaxation with TE=0
    calibrate=True,             # Derive signal scaling factor from data
    trigger=True,               # Signals are retrospectively triggered
)

# %%
# Let's see what input parameters are needed for this model:

model.print_inputs()

# %%
# For clarity and reusability we'll first define a helper 
# function which returns a dictionary with required data for a single 
# study participant:

def get_data(study, participant): 

    # --- Load the data
    file = dc.fetch(study)
    data = pydmr.read(file, 'nest')

    # --- Get the subject-level data
    roi = data['rois'][participant]
    par = data['pars'][participant]

    # --- Get GFR from screening visit if available
    if 'eGFR_abs' in par['screening']:
        eGFR = par['screening']['eGFR_abs']
    else:
        eGFR = (par['control']['eGFR_abs'] + par['drug']['eGFR_abs']) / 2

    # --- Time arrays
    time = [
        roi['control']['time_1'] - roi['control']['time_1'][0],
        roi['drug']['time_1'] - roi['drug']['time_1'][0],
    ]

    data = {     

        # Electromagnetic
        'R1_b': (1 / par['control']['T1_aorta_1'] + 1 / par['drug']['T1_aorta_1']) / 2, 
        'R1_li':(1 / par['control']['T1_liver_1'] + 1 / par['drug']['T1_liver_1']) / 2,

        # Hyperparameter
        'dt': 0.5,

        # Indicator
        'agent': 'gadoxetate',
        'BAT_1': dc.estimate_bat(time[0], roi['control']['aorta_1']),
        'BAT_2': dc.estimate_bat(time[1], roi['drug']['aorta_1']),

        # Physiological
        'GFR': eGFR / 60,

        # Sequence
        'FA': par['control']['FA_1'],
        'field_strength': 3,
        'Nk0': int(np.round(time[0][1] / par['control']['TR'] / 2)),
        'Nph': int(np.round(time[0][1] / par['control']['TR'])),
        'TR': par['control']['TR'],

        # Whole body
        'vol_1_li': par['control']['liver_volume'],
        'vol_2_li': par['drug']['liver_volume'],
        'weight':(par['control']['weight'] + par['drug']['weight']) / 2, 
    }

    idx = 0
    for visit in ['control', 'drug']:
        for scan in [1]:
            idx += 1

            # Indicator group
            data[f'rate_{idx}'] = 1
            data[f'dose_{idx}'] = par[visit][f'dose_{scan}']

            # Signal group
            data[f'nb_{idx}'] = int(par[visit]['t0'] / (time[idx - 1][1] - time[idx - 1][0]))
            for r in ['aorta', 'liver']:
                data[f'tS_{idx}_{r[:2]}'] = time[idx - 1]
                data[f'S_{idx}_{r[:2]}'] = roi[visit][f'{r}_{scan}']
                data[f'iStrig_{idx}_{r[:2]}'] = roi[visit][f'{r}_{scan}_accept']
                     
    return data


# %%
# Fitting the model
# -----------------

# --- Source data identifier
study = 'tristan_humans_healthy_rifampicin'

# --- Format the data
data = get_data(study, 'LDS-002')

# --- Fit the model
result = model(data, verbose=2)

# %%
# Verify that the optimization has converged to a solution:

# --- Update the data
data |= result['popt'] 

# --- Plot the fits
model.plot(data)

# %%
# The model first the data well, so we can now consider the 
# values for the derived parameters
dc.print_quantities(result['pder'], 'Drug effects', digits=2)

# sphinx_gallery_start_ignore
# sphinx_gallery_thumbnail_number = -1
# sphinx_gallery_end_ignore
