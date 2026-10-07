"""
.. _example_rat_liver_repeatability:

==============================
Liver function reproducibility
==============================

This example illustrates the use of `~dcmri.Liver` in a preclinical 
setting, by replicating key results from 
`Gunwhy et al (2024) <https://doi.org/10.1007/s10334-024-01192-5>`_.

The study aimed to identify the main sources of
variability in DCE-MRI biomarkers of hepatocellular function in rats. This was
done by comparing data measured at 3 different centres and 2, field strengths, at
different days in the same subjects, and over the course of several months
in the same centre.
"""

# %%
# Setup
# -----

# %% 
# Import the required packages

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pydmr
import dcmri as dc

# %%
# Fetch and read the data

data_file = dc.fetch('tristan_rats_healthy_reproducibility')
all_data = pydmr.read(data_file, 'nest')


# %%
# The basic modelling approach is illustrated in a :ref:`separate 
# case study <example_gadoxetate_rat>` so we just replicate it here:

# --- Configure the inverse model
liver = dc.InverseLiver(kinetics='1I-IC-HF', calibrate=True)

# --- Data dictionary for a given study
def liver_data(subject, visit):

    # --- Get the data for the subject and visit
    roi = all_data['rois'][subject][visit]
    par = all_data['pars'][subject][visit]

    # --- Generate the input function 
    dt = 0.5
    bat = par['BAT'] + roi['time'][1] / 2
    t = np.arange(0, np.amax(roi['time']) + 180, dt)
    ca = dc.tristan_rat(t, BAT=bat, duration=par['duration'])

    # --- Number of phase lines for a triggered sequence
    ts = roi['time'][1] - roi['time'][0]
    Nph = int(np.round(ts / par['TR'])) 

    # --- Return the data dictionary 
    return {
        'tS_li': roi['time'],
        'S_li': roi['liver'],
        'agent': 'gadoxetate',
        'ci_li': ca,
        'field_strength': par['field_strength'],
        'TR': par['TR'],
        'FA': par['FA'],
        'Nph': Nph, 
        'Nk0': int(np.round(Nph / 2)) ,
        'dt': dt,
        'nb': par['n0'],
        'H': 0.418,           # Cremer et al, J Cereb Blood Flow Metab 3, 254-256 (1983)
        'v_e_li': 0.23,
        'v_li': 1.0,
        'pfree': {'k_e2h':[0, 1], 'T_h': [0, 60 * 60]},
    }

# %%
# Computation
# -----------
# Now we can analyse all data in the database.

# --- Fit all datasets and save results in a list
records = []
for subj, visits in all_data['rois'].items():
    for visit in visits:
        inputs = liver_data(subj, visit)
        result = liver(inputs) 
        study_data = all_data['pars'][subj][visit]

        for parameter, value in result['pder'].items():
            records.append({
                'subject': subj,
                'study': study_data['study'],
                'visit': study_data['visit'],
                'parameter': parameter,
                'value': value,
            })

# --- Convert to dataframe for analysis
results = pd.DataFrame(records)

# --- The result is a data table in long format:
print(results.to_string())


# %%
# Plot results
# ------------
# We visualise the results by plotting the 95% confidence intervals 
# for the two main biomarkers per substudy. The mean and 95% CI on the 
# mean are shown in color for reference. 

# Customise plot settings
plt.rcParams['savefig.dpi'] = 300
plt.rcParams["axes.labelsize"] = 50
plt.rcParams["axes.titlesize"] = 50
plt.rcParams["axes.labelweight"] = 'bold'
plt.rcParams["axes.titleweight"] = 'bold'
plt.rcParams["font.weight"] = 'bold'
plt.rc('axes', linewidth=2)
plt.rc('xtick', labelsize=40)
plt.rc('ytick', labelsize=40)
plt.rcParams["lines.linewidth"] = 4
plt.rcParams['lines.markersize'] = 12

# Create list of biomarkers (parameters) of interest
params = ['k_e2h', 'k_h2b']

# Extract data of interest, i.e., visit 1 data for parameters of interest
data = results.query('parameter in @params and visit==1')
data['value'] *= 6000 # to units of mL/min/100cm3

# Get statistical summaries per parameter and study group
stat_summary = data.groupby(['parameter', 'study'])['value'].agg(['mean'])

# Calculate benchmark values per parameter by averaging all study group averages
benchmarks = stat_summary.groupby(['parameter'])['mean'].agg(['mean', 'sem'])

# Calculate the 95% confidence intervals for each parameter benchmark
benchmarks['CI95'] = benchmarks['sem'].mul(1.96)

# Panel order, left to right, with matching y-limits and labels
order = ['k_e2h', 'k_h2b']
ylims = [(0, 300), (0, 30)]
ylabels = ['$k_{e2h}$', '$k_{h2b}$']

g = sns.catplot(data=data,
                x='study',
                y='value',
                col='parameter',
                col_order=order,
                kind='point',
                capsize=0.2,
                sharey=False,
                linestyle='none',
                height=14,
                aspect=1.2,
                color='k',
                errorbar=('ci', 95))

g.set_titles("")

# Overlay y-labels, y-limits and benchmark lines on each panel
for ax, par, ylim, ylabel in zip(g.axes[0], order, ylims, ylabels):
    mean = benchmarks.loc[par, 'mean']
    ci = benchmarks.loc[par, 'CI95']
    ax.set(ylim=ylim)
    ax.set_ylabel(f"{ylabel} [mL/min/100cm3]")
    ax.axhline(mean, color='blue', ls=':')
    ax.axhline(mean - ci, color='red', ls='--')
    ax.axhline(mean + ci, color='red', ls='--')

plt.tight_layout()
plt.show()

# %%
# Discussion
# ----------
# The results replicate the main finding from the paper, that there 
# are substantial study-dependent biases in absolute values.

# sphinx_gallery_start_ignore
# Choose the last image as a thumbnail for the gallery
# sphinx_gallery_thumbnail_number = -1
# sphinx_gallery_end_ignore
