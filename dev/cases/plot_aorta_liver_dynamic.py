"""
=================
AortaLiverDynamic
=================

These example shows the use of the `~dcmri.AortaLiverDynamic` model to 
simultaneously fit signals measured in aorta and liver over two separate scans 
on the same day. 
"""

# %%
# Setup
# -----

# Import packages
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

# %%
# Set up the model
# ----------------
# We need to decide how to configure the model, so let's 
# see what options are available:

dc.AortaLiverDynamic.print_configs()

# %%
# For these data we will use the general model for an intracellular 
# tracer, with non-stationary uptake function and a standard 3D-SPGR-SS sequence:

config = {
    'kinetics': '1I-IC',
    'sequence': '3D-SPGR-SS',
    'non_stationary': 'U',
}

# %%
# Print the fixed parameters of this configuration: 

dc.AortaLiverDynamic(**config).print_params(round_to=3, fixed_only=True)

# %%
# Model definition
# ----------------
# In order to avoid some repetition in this script, we define a function that 
# returns a trained model for a single dataset with 2 scans:

# --- Get the time arrays to find the maximum time
time_1 = roi['time_1'] - roi['time_1'][0]
time_2 = roi['time_2'] - roi['time_1'][0]

# --- Initialise the model with known defaults
aol_model = dc.AortaLiverDynamic(

    # Indicator quantities
    agent = 'gadoxetate',
    dose_1 = par['dose_1'],
    dose_2 = par['dose_2'],
    rate = 1,

    # Signal quantities
    FA = par['FA_1'],
    FA_2 = par['FA_2'],
    field_strength = 3,
    t_scan2 = time_2[0],
    TR = par['TR'],
    TS = time_1[1],

    # Electromagnetic quantities
    R10_a = 1/par['T1_aorta_1'],
    R10_l = 1/par['T1_liver_1'],

    # Physiological quantities
    weight = par['weight'],
    vol_l = par['liver_volume'],

    # Hyperparameter quantities
    tmax = max(time_2),
    
    # Configuration
    **config 
)

# %%
# Fitting the model
# -----------------

# --- Baseline
n0 = int(par['t0']/time_1[1])

# --- Time points in aorta and liver
time = (
    time_1[roi['aorta_1_accept']], 
    time_2[roi['aorta_2_accept']], 
    time_1[roi['liver_1_accept']],
    time_2[roi['liver_2_accept']],
)

# --- Signal in aorta and liver
signal = (
    roi['aorta_1'][roi['aorta_1_accept']], 
    roi['aorta_2'][roi['aorta_2_accept']], 
    roi['liver_1'][roi['liver_1_accept']],
    roi['liver_2'][roi['liver_2_accept']],
)

# --- Train the model
R102a, R102l = 1/par['T1_aorta_3'], 1/par['T1_liver_3']
aol_model.train(time, signal, R102a=R102a, R102l=R102l, n0=n0, xtol=1e-3)

# --- Verify that the model fits the data
aol_model.plot(time, signal)

# %%
# Check results
# -------------
aol_model.print_params(round_to=3, group='phys', deriv=True)


# sphinx_gallery_start_ignore
# sphinx_gallery_thumbnail_number = -1
# sphinx_gallery_end_ignore