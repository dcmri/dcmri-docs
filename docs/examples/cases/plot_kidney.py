"""
======
Kidney
======

This example illustrates the use of `~dcmri.Kidney` for measurement of 
single-kidney glomerular filtration rate (SK-GFR). We will analyse 
one kidney of a participant in the KRUK study.
"""

# %%
# Setup
# -----

# --- Import packages
import pydmr
import dcmri as dc

# --- The dataset to be analysed
kidney, participant, visit = 'LK', '001', 'pre'
# kidney, participant, visit = 'RK', '044', 'pre' # Outlier

# --- Fetch the data
datafile = dc.fetch('KRUK')
dmr = pydmr.read(datafile, 'nest')
roi = dmr['rois'][participant][visit] 
par = dmr['pars'][participant][visit] 

# %%
# Identify a configuration
# ------------------------
# Let's see what options we have to configure the model:

dc.Kidney.print_configs()

# %%
# We'll use a 2-compartment filtration model for the kidney and 
# assume acquisition with a 3D-SPGR-SS sequence:

config = {
    'kinetics': '2CF',
    'sequence': '3D-SPGR-SS'
}

# %%
# Next we need to set suitable values for the constant parameters, 
# so lets print out the default state for this configuration: 

dc.Kidney(**config).print_params(round_to=3, fixed_only=True)

# %%
# Initialise a Kidney model
# -------------------------

# --- B0 and precontrast T1
B0 = par['field_strength']
T1 = par[f'{kidney} T1'] if f'{kidney} T1' in par else dc.T1(B0, 'kidney')

# --- Define kidney model
kidney_model = dc.Kidney(

    # Indicator quantities
    agent=par['agent'],

    # Signal quantities
    field_strength=B0,
    FA=par['FA'],
    TR=par['TR'],

    # Electromagnetic quantities
    R10=1 / T1,

    # Configuration
    **config
)

# %%
# Train the Kidney model
# ----------------------

# --- Get the kidney data
time, signal = roi['time'], roi[kidney]

# --- Define the AIF
aif = {'signal': roi['aorta'], 'R10': 1/dc.T1(B0, 'blood')}

# --- Train the kidney model on the data
kidney_model.train(time, signal, aif=aif, n0=par['n0'], bounds={'Tt': [30, 300]})

# --- Plot the results to check that the model has fitted the data
kidney_model.plot(time, signal)

# %%
# Numerical results
# -----------------
# Print the measured model parameters:

kidney_model.print_params(round_to=3, free_only=True)

#%%
# Compare the measured SK-GFR to the 
# radio-isotope reference value:

FF, Fp = kidney_model.params('FF', 'Fp')
iso_sk_gfr = dmr['pars'][participant][visit][f'{kidney} iso-SK-GFR']
mrr_sk_gfr = FF * Fp * par[f'{kidney} vol']

print(f"Radio-isotope SK-GFR: {round(60 * iso_sk_gfr)} mL/min")
print(f"MRR SK-GFR: {round(60 * mrr_sk_gfr)} mL/min")


# sphinx_gallery_start_ignore
# Choose the last image as a thumbnail for the gallery
# sphinx_gallery_thumbnail_number = -1
# sphinx_gallery_end_ignore

