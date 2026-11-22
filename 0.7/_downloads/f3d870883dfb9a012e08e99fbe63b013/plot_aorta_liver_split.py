"""
============================
Aorta and Liver in two scans
============================

These example shows the use of the `~dcmri.AortaLiverSplit` model to 
simultaneously fit signals measured in aorta and liver over two 
different scans on the same day. 
"""

import numpy as np
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
    estimate_bat='custom',      # Use the dedicated BAT estimator
)

# %%
# Let's see what input parameters are needed for this model:

model.print_inputs()

# %%
# Fitting the model
# -----------------

# --- Source data identifier
study = 'tristan_humans_healthy_rifampicin'

# --- Format the data
visit_1_data = dc.load_tristan_humans(study, 'LDS-002', visits=['control'])
visit_2_data = dc.load_tristan_humans(study, 'LDS-002', visits=['drug'])

# --- Fit the model
visit_1_result = model(visit_1_data, verbose=2)
visit_2_result = model(visit_2_data, verbose=2)

# %%
# Verify that the optimization has converged to a solution:
model.plot(visit_1_data, visit_1_result)
model.plot(visit_2_data, visit_2_result)

# %%
# The model first the data well, so we can now consider the 
# values for the derived parameters
dc.print_quantities(visit_1_result['pars'], 'Control visit', digits=2)
dc.print_quantities(visit_2_result['pars'], 'Drug visit', digits=2)

# sphinx_gallery_start_ignore
# sphinx_gallery_thumbnail_number = -1
# sphinx_gallery_end_ignore
