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

# --- Load the data
data = dc.load_tristan_humans(study, 'LDS-002', scans=[1])

# --- Fit the model
result = model(data, verbose=2)

# %%
# Verify that the optimization has converged to a solution:

# --- Plot the fits
model.plot(data, result)

# %%
# The model first the data well, so we can now consider the 
# values for the derived parameters
dc.print_quantities(result['pars'], 'Drug effects', digits=2)

# sphinx_gallery_start_ignore
# sphinx_gallery_thumbnail_number = -1
# sphinx_gallery_end_ignore
