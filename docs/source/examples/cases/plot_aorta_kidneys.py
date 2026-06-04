"""
============
AortaKidneys
============

These example shows the use of the `~dcmri.AortaKidneys` model to 
fit signals measured in aorta and both kidneys simultaneously. 
"""

# %%
# Import packages
# ---------------

import numpy as np
import pydmr
import dcmri as dc

# %%
# Datasets
# --------
# We will use the mini-pig kidney data to illustrate the use of the model.

dmrfile = dc.fetch('minipig_renal_fibrosis')
data = pydmr.read(dmrfile, 'nest')
rois, pars = data['rois']['Pig']['Test'], data['pars']['Pig']['Test']
time = pars['TS'] * np.arange(len(rois['Aorta']))

# %%
# Set up the model
# ----------------
# We need to decide how to configure the model, so let's 
# see what options are available:

dc.AortaKidneys.print_configs()

# %%
# Let's choose a chain model for the heart-lung system 
# and a single compartment for the organs. We will model the kidneys with 
# a 2-compartment filtration model, and we know that the contrast agent 
# used does not have liver clearance. The acquisition is done 
# with a 3D-SPGR sequence in steady-state (3D-SPGR-SS), but since we expect some level 
# of inflow corruption in these data we will use the inflow-corrected version 
# of the model (3D-SPGR-SSI). 
#
# With these choices the configuration becomes:

config = {
    'heartlung': 'chain',
    'organs': 'comp',
    'kidneys': '2CF',
    'sequence': '3D-SPGR-SSI',
    'liver_clearance': False,
}

# %%
# Next we need to set suitable values for the fixed parameters, 
# so lets see what they are for this configuration: 

dc.AortaKidneys(**config).print_params(round_to=3, fixed_only=True)

# %%
# Initialise the model
# --------------------
# We initialize the model, setting values for all parameters 
# where we have better defaults available. In this example the kidney 
# volumes are not actually known, so for the purpose of illustration
# we use a typical value of 85mL: 

aorta_kidneys = dc.AortaKidneys(

    # Indicator quantities
    dose=pars['dose'],
    rate=pars['rate'],

    # Signal quantities
    FA=pars['FA'],
    field_strength=pars['B0'],
    TR=pars['TR'],
    TS=pars['TS'],

    # Electromagnetic quantities
    R10_a=1/dc.T1(pars['B0'], 'blood'),
    R10_lk=1/dc.T1(pars['B0'], 'kidney'),
    R10_rk=1/dc.T1(pars['B0'], 'kidney'),

    # Physiological quantities
    vol_lk=85,
    vol_rk=85,
    weight=pars['weight'],

    # Configuration
    **config
)

# %%
# Fitting the model
# -----------------

# Define signal data
signal = (rois['Aorta'], rois['LeftKidney'], rois['RightKidney'])

# Train model
aorta_kidneys.train(time, signal, n0=pars['n0'])

# Check the fit to the data
aorta_kidneys.plot(time, signal)

# %%
# Check results
# -------------
aorta_kidneys.print_params(round_to=3, free_only=True)


# sphinx_gallery_start_ignore
# sphinx_gallery_thumbnail_number = -1
# sphinx_gallery_end_ignore