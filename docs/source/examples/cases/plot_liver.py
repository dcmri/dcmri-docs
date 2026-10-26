"""
.. _example_gadoxetate_rat:

=====
Liver
=====

Using `~dcmri.Liver` to measure hepatocellular function in rats.

This example illustrates the use of `~dcmri.Liver` with case studies, 
measuring liver function in rats on Day 1 (control) and on Day 2 (after 
administration of an inhibitor drug). A separate example shows a complete 
:ref:`analysis of all data <example_tristan_preclinical>`
"""

# %%
# Setup
# -----

# --- Import packages
import numpy as np
import pydmr
import dcmri as dc


# %%
# Modelling
# ---------
# This study uses an intracellullar agent, and in rats the mixing in 
# the blood pool is fast, so we use a single inlet model (1I) for an 
# intracellular agent (IC) with high flow (HF). We also want to use 
# a calibrated model so S0 is derived from the data. All other 
# default configurations are fine so don't need to be specified 
# explicitly:
liver = dc.InverseLiver(kinetics='1I-IC-HF', calibrate=True)

# %%
# Let's see what input parameters are needed for this model:

liver.print_inputs()

# %%
# Since we will be running this on different datasets, we first 
# define a function which returns the data dictionary for a given 
# dataset:

def get_data(study, subject, visit):

    # --- Load the data
    data = dc.load_tristan_rats(study, subject, visit)

    # --- Define time points for simulation
    dt = 0.5
    tmax = np.amax(data['tS_li']) + 120
    t = np.arange(0, tmax, dt)

    const = {
        # --- Input function
        'ci_li': dc.tristan_rat(t, BAT=data['BAT'], duration=data['duration']),

        # --- Hyperparameters
        'dt': dt,

        # --- Physiological constants
        # The volume fractions are treated as constants since prior 
        # sensitivity analysis has shown they are not measureable from 
        # these data. Also they are not expected to change after 
        # drug administration so fixing them should not greatly affect
        # measured treatment effects.

        'H': 0.418, # Cremer et al, JCBFM 3, 254-256 (1983)
        'v_e_li': 0.23,
        'v_li': 1.0,

        # --- Free parameters
        # The primary endpoints of this study are treated as free 
        # parameters with liberal constraints so results are fully 
        # data driven:
        'pfree': {'k_e2h':[0, 1], 'T_h': [0, 60 * 60]},
    }

    return data | const


# %%
# Case study 1 - strong inhibition
# --------------------------------
# For the first case study, we choose a subject from study 08 
# where all rats received a standard dose of cyclosporine 
# on the second day. The study showed this to be a strong inhibitor 
# of uptake and excretion:

study = 'tristan_rats_study_08_single_cyclosporine'

# --- Get the data
day_1_data = get_data(study, 'S08-02', 'Day_1')
day_2_data = get_data(study, 'S08-02', 'Day_2')

# --- Fit the models
day_1_result = liver(day_1_data)
day_2_result = liver(day_2_data)

# %%
# Before we interpret the results, let's verify the optimization has 
# converged to a solution:

# --- Update the data
day_1_data |= day_1_result['popt']
day_2_data |= day_2_result['popt']

# --- Plot the fits
liver.plot(day_1_data)
liver.plot(day_2_data)

# %%
# The model first the data well, so we can now consider the 
# values for the derived parameters
dc.print_quantities(day_1_result['pars'], 'Day 1', digits=2)
dc.print_quantities(day_2_result['pars'], 'Day 2', digits=2)

# %%
# The values confirm the strong inhibition of liver function by the 
# drug. The hepatocellular uptake rate (k_e2h) has dropped from 0.030 
# to 0.0039 mL/sec/cm3, and the biliary excretion rate (k_h2b) from 
# 0.0022 to 0.00098 mL/sec/cm3.

# %%
# Case study 2 - weak inhibition
# ------------------------------
# For the second case study we analyse data from study 06 where all 
# rats received a dose of pioglitazone of the second day. The study 
# showed this to be a weak inhibitor of excretion with no effect on 
# uptake:

study = 'tristan_rats_study_06_single_pioglitazone'

# --- Get the data
day_1_data = get_data(study, 'S06-02', 'Day_1')
day_2_data = get_data(study, 'S06-02', 'Day_2')

# --- Fit the models
day_1_result = liver(day_1_data)
day_2_result = liver(day_2_data)

# %%
# As before, always good to check the fit before interpreting the 
# results:

# --- Update the data
day_1_data |= day_1_result['popt']
day_2_data |= day_2_result['popt']

# --- Plot the fits
liver.plot(day_1_data)
liver.plot(day_2_data)

# %%
# Again we can verify the model fits the data well. Let's have 
# a look at the values for the derived parameters:
dc.print_quantities(day_1_result['pars'], 'Day 1', digits=2)
dc.print_quantities(day_2_result['pars'], 'Day 2', digits=2)

# %%
# The values confirm the very weak effect of the drug on liver 
# function. The hepatocellular uptake rate (k_e2h) has dropped from 
# 0.032 to 0.030 mL/sec/cm3, and the biliary excretion rate (k_h2b) 
# from 0.0029 to 0.0024 mL/sec/cm3.

# sphinx_gallery_start_ignore
# Choose the last image as a thumbnail for the gallery
# sphinx_gallery_thumbnail_number = -1
# sphinx_gallery_end_ignore
