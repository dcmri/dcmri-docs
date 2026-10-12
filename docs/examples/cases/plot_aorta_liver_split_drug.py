"""
==============================
Liver Drug effect in two scans
==============================

These example shows the use of the `~dcmri.AortaLiverSplitDrug` model to 
simultaneously fit signals measured in aorta and liver over two 
different days, with two scans on each day. The second day, an 
inhibitor drug is administered before the first scan of the day.
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

model = dc.InverseAortaLiverSplitDrug(
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
# Fitting the model
# -----------------

# --- Source data identifier
study = 'tristan_humans_healthy_rifampicin'

# --- Load the data
data = dc.load_tristan_humans(study, 'LDS-002')

# --- Estimate BAT
data |= {
    'BAT_1': dc.estimate_bat(data['tS_1_ao'], data['S_1_ao']),
    'BAT_2': data['tS_2_ao'][np.argmax(data['S_2_ao'])],
    'BAT_3': dc.estimate_bat(data['tS_3_ao'], data['S_3_ao']),
    'BAT_4': data['tS_4_ao'][np.argmax(data['S_4_ao'])],
}

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
dc.print_quantities(result['pder'], 'Drug effect', digits=2)


# sphinx_gallery_start_ignore
# sphinx_gallery_thumbnail_number = -1
# sphinx_gallery_end_ignore
