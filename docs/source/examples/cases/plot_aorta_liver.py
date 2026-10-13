"""
===============
Aorta and Liver
===============

These example shows the use of the `~dcmri.AortaLiver` model to 
fit signals measured in aorta and liver simultaneously. 

"""
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
    estimate_bat='custom',      # Use the dedicated BAT estimator
)

# %%
# Let's see what input parameters are needed for this model:

aol.print_inputs()

# %%
# Fitting the model
# -----------------
study = 'tristan_humans_healthy_rifampicin'

# --- Format the data for on subject
visit_1_data = dc.load_tristan_humans(study, 'LDS-002', visits=['control'], scans=[1])
visit_2_data = dc.load_tristan_humans(study, 'LDS-002', visits=['drug'], scans=[1])

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
