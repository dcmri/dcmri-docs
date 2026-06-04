"""
=====================================================
Preclinical - repeat dosing effects on liver function
=====================================================

`Ebony Gunwhy <https://orcid.org/0000-0002-5608-9812>`_.

This example illustrates the use of `~dcmri.Liver` for fitting of signals 
measured in liver. The use case is provided by the liver work package of the 
`TRISTAN project <https://www.imi-tristan.eu/liver>`_  which develops imaging 
biomarkers for drug safety assessment. The manuscript relating to this data
and analysis is currently in preparation. 

The specific objective of the study was to investigate the potential of
gadoxetate-enhanced DCE-MRI to study acute inhibition of hepatocyte
transporters of drug-induced liver injury (DILI) causing drugs, and to study
potential changes in transporter function after chronic dosing.

The study presented here measured gadoxetate uptake and excretion in healthy 
rats scanned after administration of vehicle and repetitive dosing regimes
of either Rifampicin, Cyclosporine, or Bosentan. Studies were performed in
preclinical MRI scanners at 3 different centers and 2 different field strengths.

**Reference**

Mikael Montelius, Steven Sourbron, Nicola Melillo, Daniel Scotcher, 
Aleksandra Galetin, Gunnar Schuetz, Claudia Green, Edvin Johansson, 
John C. Waterton, and Paul Hockings. Acute and chronic rifampicin effect on 
gadoxetate uptake in rats using gadoxetate DCE-MRI. Int Soc Mag Reson Med 
2021; 2674.
"""

# %%
# Setup
# -----

# --- Import packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pydmr
import dcmri as dc

# --- Fetch the data
dmrfile = dc.fetch('tristan_rats_healthy_multiple_dosing')
data = pydmr.read(dmrfile, 'nest')
rois, pars = data['rois'], data['pars']


# %%
# Model definition
# ----------------
# In order to avoid some repetition in this script, we define a function that 
# returns a trained model for a single dataset. 
# 
# The model uses a standardized, population-average input function and fits 
# for only 2 parameters, fixing all other free parameters to typical values 
# for this rat model:

def tristan_rat(roi, par, **kwargs):

    # --- Generate an input function
    dt = 0.5
    t = np.arange(0, np.amax(roi['time']) + dt, dt)
    ca = dc.tristan_rat(t, BAT=par['BAT'], duration=par['duration'])

    # --- Set up a liver model
    liver_model = dc.Liver(

        # Configuration
        kinetics = '1I-IC',
        sequence = '3D-SPGR-SS',
        non_stationary = None,

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
    )

    # Train the model
    free = {'E': [0.0, 0.9], 'Th': [0, 60 * 60]}
    _, sdev, _ = liver_model.train(roi['time'], roi['liver'], n0=par['n0'], free=free, **kwargs)

    # Export the numerical parameters, including derived
    # pars = liver_model.export_params(sdev=sdev, num_only=True, scalar_only=True, deriv=True)
    pars = liver_model.export_params(sdev=sdev, group='phys', deriv=True)

    # Return as dataframe
    df = pd.DataFrame.from_dict(pars, orient='index')
    return df.reset_index().rename(columns={'index': 'parameter'})


# %%
# Fit all data
# ------------
# Now that we have defined the model, we proceed 
# with fitting all the data. Results are stored in a dataframe in long format:

results = []

# Loop over all datasets
for subj in rois.keys():
    for visit in rois[subj].keys():

        roi = rois[subj][visit]
        par = pars[subj][visit]

        # Train the model and get the results
        df = tristan_rat(roi, par, xtol=1e-3)
        
        # Add study, visit and subject info
        df['subject'] = subj
        df['study'] = par['study']
        df['visit'] = par['visit']

        # Add to the list of all results
        results.append(df)

# Combine all results into a single dataframe
results = pd.concat(results).reset_index(drop=True)

# Print all results
print(results.to_string())


# %%
# Plot individual results
# -----------------------
# Now let's plot the biomarker values across visits for each study group.
# For this exercise, let's specify Ktrans and kbh as the biomarker parameters that
# we are interested in. For each subject, we can visualise the change in
# biomarker values between visits. For reference, in the below plots, the
# studies are numbered as follows:
# Study 1: Rifampicin repetitive dosing regime
# Study 2: Cyclosporine repetitive dosing regime
# Study 3: Bosentan repetitive dosing regime

# Customise plot settings
plt.rcParams["axes.titlesize"] = 25
plt.rcParams["axes.labelsize"] = 20
plt.rcParams["axes.labelweight"] = 'bold'
plt.rcParams["axes.titleweight"] = 'bold'
plt.rcParams["font.weight"] = 'bold'
plt.rc('axes', linewidth=1.5)
plt.rc('xtick', labelsize=15)
plt.rc('ytick', labelsize=15)
plt.rcParams["lines.linewidth"] = 1.5
plt.rcParams['lines.markersize'] = 2

# Extract results of interest, i.e., for parameters khe and kbh
filtered_data = results.query("parameter == 'Ktrans' | parameter == 'kbh'")
filtered_data['value'] *= 6000 # to units of mL/min/100cm3

# Plot distributions across visits per study groups and per biomarker
g = sns.catplot(data=filtered_data,
                x='visit',
                y='value',
                palette='rocket',
                hue='subject',
                row='parameter',
                col='study',
                kind='point',
                sharey=False)

g.set_titles(pad=15) 

# Set limits for y-axes
for i in range(0, 3):
    g.axes[0, i].set(ylim=([0, 200]))
    g.axes[1, i].set(ylim=([0, 30]))

g.set_ylabels("Value [mL/min/100cm3]") 

# reposition legend
sns.move_legend(g, "lower right", bbox_to_anchor=(0.95, 0.7))

plt.tight_layout()
plt.show()

# Choose the last image as a thumbnail for the gallery
# sphinx_gallery_thumbnail_number = -1
