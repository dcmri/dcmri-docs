"""
==========
AortaLiver
==========

These example shows the use of the `~dcmri.AortaLiver` model to 
fit signals measured in aorta and liver simultaneously. 
"""

# %%
# Setup
# -----

# --- Import packages
import pydmr
import dcmri as dc

# --- Fetch the data
dmrfile = dc.fetch('tristan_humans_healthy_rifampicin')
data = pydmr.read(dmrfile, 'nest')

# --- Identify the case
participant, visit = '002', 'control'

# --- Get the subject-level data
roi = data['rois'][participant][visit]
par = data['pars'][participant][visit]
time = roi['time_1'] - roi['time_1'][0]


# %%
# Set up the model
# ----------------
# We need to decide how to configure the model, so let's 
# see what options are available:

dc.AortaLiver.print_configs()

# %%
# For these data we will use the general model for an intracellular 
# tracer, with stationary function and a standard 3D-SPGR-SS sequence:

config = {
    'kinetics': '1I-IC',
    'sequence': '3D-SPGR-SS',
    'non_stationary': None,
}

# %%
# Print the fixed parameters of this configuration: 

dc.AortaLiver(**config).print_params(round_to=3, fixed_only=True)

# %%
# Model definition
# ----------------
# Now define the model with all parameters set:

aol_model = dc.AortaLiver(          

    # Indicator quantities
    agent = 'gadoxetate',
    dose = par['dose_1'],
    rate = 1,

    # Signal quantities
    field_strength = 3,
    TR = par['TR'],
    FA = par['FA_1'],
    TS = time[1],
    
    # Electromagnetic quantities
    R10_a = 1/par['T1_aorta_1'],
    R10_l = 1/par['T1_liver_1'],

    # Physiological quantities
    weight = par['weight'],

    # Hyperparameter quantities
    tmax = max(time),
    vol_l = par['liver_volume'],
    
    # Configuration
    **config 
)

# %%
# Fitting the model
# -----------------

# --- Baseline
n0 = int(par['t0']/time[1])

# --- Time points in aorta and liver
time = (
    time[roi['aorta_1_accept']], 
    time[roi['liver_1_accept']],
)

# --- Signal in aorta and liver
signal = (
    roi['aorta_1'][roi['aorta_1_accept']], 
    roi['liver_1'][roi['liver_1_accept']],
)

# --- Train the model
aol_model.train(time, signal, n0=n0, xtol=1e-3)

# --- Verify that the model fits the data
aol_model.plot(time, signal)

# %%
# Check results
# -------------
aol_model.print_params(round_to=3, group='phys', deriv=True)


# sphinx_gallery_start_ignore
# sphinx_gallery_thumbnail_number = -1
# sphinx_gallery_end_ignore
