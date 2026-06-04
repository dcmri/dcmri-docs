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

# --- The dataset to be analysed
case = 'S12-02'

# --- Fetch the data
dmrfile = dc.fetch('tristan_rats_healthy_six_drugs')
dmr = pydmr.read(dmrfile, 'nest')

# %%
# Identify a configuration
# ------------------------
# Let's see what options we have to configure the model:

dc.Liver.print_configs()

# %%
# This study uses an intracellullar agent, and in rats the mixing in 
# the blood pool is fast, so we will use a single inlet model (1I). 
# In a single acquisition there is no good rationale for allowing 
# non-stationary function, and the acquisition in this study is done 
# with a 3D-SPGR sequence in steady-state. 
# 
# So we are left with the following configuration:

config = {
    'kinetics': '1I-IC',
    'sequence': '3D-SPGR-SS',
    'non_stationary': None,
}

# %%
# Let's see what parameters define the state: 

dc.Liver(**config).print_params(round_to=3)

# %%
# Train a Liver model
# ------------------------
# The measured input functions in this study are unstable so we will 
# analyse the data with a standardised input function. For the 
# liver model in this case we fix a number of physiological 
# parameters to literature value as they are not expected to change 
# much. 
# 
# We are going to analyse two datasets so let's pack up this 
# part in a helper function:

def train_rat_liver(roi, par):

    # --- Generate an input function
    dt = 0.5
    t = np.arange(0, np.amax(roi['time']) + dt, dt)
    ca = dc.tristan_rat(t, BAT=par['BAT'], duration=par['duration'])

    # --- Set up a liver model
    liver_model = dc.Liver(

        # Indicator quantities
        agent = 'gadoxetate',
        c_a = ca,

        # Signal quantities
        field_strength = par['field_strength'],
        TR = par['TR'],
        FA = par['FA'],

        # Electromagnetic quantities
        R10 = 1/dc.T1(par['field_strength'], 'liver'),

        # Physiological quantities
        Fp = 0.022,      # doi: 10.1021/acs.molpharmaceut.1c00206
        H = 0.418,       # Cremer et al, J Cereb Blood Flow Metab 3, 254-256 (1983)
        ve = 0.23,

        # Hyperparameter quantities
        dt = dt,

        # Configuration
        **config
    )

    # --- Define free parameters
    free = {'E': [0.0, 0.9], 'Th': [0, 60 * 60]}

    # --- Train the model
    liver_model.train(roi['time'], roi['liver'], n0=par['n0'], free=free)

    return liver_model

# %%
# Analyse the Day 1 data
# ----------------------

# --- Get the data
roi = dmr['rois'][case]['Day_1']
par = dmr['pars'][case]['Day_1']

# --- Train the model on the data
liver_model = train_rat_liver(roi, par)

# --- Check that the model has fitted the data
liver_model.plot(roi['time'], roi['liver'])

# %%
# Print the measured model parameters. 

liver_model.print_params(round_to=4, deriv=True, group='phys')

# %%
# Analyse the Day 2 data
# ----------------------

# --- Get the data
roi = dmr['rois'][case]['Day_2']
par = dmr['pars'][case]['Day_2']

# --- Train the model on the data
liver_model = train_rat_liver(roi, par)

# --- Plot the results to check that the model has fitted the data
liver_model.plot(roi['time'], roi['liver'])


# %%
# Day 1 results
# -------------
# Print the measured model parameters. 

liver_model.print_params(round_to=4, deriv=True, group='phys')

# %%
# The values confirm the effect of the drug on liver function. The 
# liver extraction fraction of gadoxetate has dropped from 80% to 37% 
# the hepatocellular uptake rate (khe) from 0.096 to 0.013 mL/sec/cm3, and 
# the biliary excretion rate (kbh) from 0.0025 to 0.0013 mL/sec/cm3.

# sphinx_gallery_start_ignore
# Choose the last image as a thumbnail for the gallery
# sphinx_gallery_thumbnail_number = -1
# sphinx_gallery_end_ignore
