"""
.. _example_six_drugs:

===================================
Effect of 6 drugs on liver function
===================================

This example illustrates the use of `~dcmri.Liver` in a preclinical 
setting, by replicating key results from
`Melillo et al (2023) <https://doi.org/10.3390/pharmaceutics15030896>`_.  

The study determined the effect of 6 test drugs on liver function as 
measured by gadoxetate uptake and excretion in healthy 
rats. Data were collected on preclinical MRI scanners at 3 different 
centers and 2 different field strengths. 
"""

# %%
# Setup
# -----

# %% 
# Import the required packages

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pydmr
import dcmri as dc

# %%
# Fetch and read the data

data_file = dc.fetch('tristan_rats_healthy_six_drugs')
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
# Plot subject-level results
# --------------------------
# We visualise the results by plotting the drug 
# effect for all subjects, and for both biomarkers: uptake rate ``k_e2h`` and 
# excretion rate ``k_h2b``:

studies = {5: 'Asunaprevir', 10: 'Bosentan', 8: 'Cyclosporine',
           7: 'Ketoconazole', 6: 'Pioglitazone', 12: 'Rifampicin'}

clr = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown']
fs = 10
scale = 6000  # rate constants in mL/min/100mL
rows = [('k_e2h', 300), ('k_h2b', 30)]   # (parameter, y-axis maximum)

fig, ax = plt.subplots(len(rows), len(studies), figsize=(9, 8), sharey='row')
fig.subplots_adjust(wspace=0.2, hspace=0.1)

for col, (study, drug) in enumerate(studies.items()):
    ax[0, col].set_title(drug, fontsize=fs, pad=10)
    study_data = results[results.study == study]

    for row, (par, _) in enumerate(rows):
        # subjects x visits table for this parameter
        vals = (study_data[study_data.parameter == par]
                .pivot(index='subject', columns='visit', values='value'))
        for subj, v in vals.iterrows():
            ax[row, col].plot(v.index, scale * v, '-o', ms=6, label=subj,
                              color=clr[int(subj[-2:]) - 1])

# Axis formatting (y-axes are shared along each row)
for row, (par, ymax) in enumerate(rows):
    ax[row, 0].set_ylim(0, ymax)
    ax[row, 0].set_ylabel(f'{par} (mL/min/100cm3)', fontsize=fs)
    ax[row, 0].tick_params(axis='y', labelsize=fs)
for a in ax.flat:
    a.tick_params(labelbottom=False)

plt.show()

# %%
# Plot key findings
# -----------------
# We'll summarise the key findings from the study using a traffic-light 
# type visualisation:
# 
# - **red** means the inhibition is more than 20% (i.e. upper value of 
#   the 95% CI is less than -20%).
# - **orange** means the inhbition is less than 20% (i.e. upper value 
#   of the 95% CI is less than 0%).
# - **green** means no inhibition was detected with 95% confidence 
#   (i.e. 0% lies in the 95% CI).

params = ['k_e2h', 'k_h2b']

def effect_color(mean, ci):
    """Colour by the upper end of the 95% CI of the effect (in %)."""
    upper = mean + ci
    if upper < -20:
        return 'tab:red'
    if upper < 0:
        return 'tab:orange'
    return 'tab:green'

# Set up figure
fig, axes = plt.subplots(1, 2, figsize=(6, 5), sharey=True)
fig.subplots_adjust(left=0.3, right=0.7, wspace=0.25)
for ax, par in zip(axes, params):
    ax.set_title(f'{par} effect (%)', fontsize=fs, pad=10)
    ax.set_xlim(-100, 50)
    ax.grid(which='major', axis='x', linestyle='-')

# Loop over all studies
for study, drug in studies.items():
    study_data = results[results.study == study]

    # One pivot for both visits: columns are (visit, parameter)
    wide = study_data.pivot_table(index='subject', columns=['visit', 'parameter'],
                                  values='value')

    # Effect of the drug in % (subjects x parameters)
    effect = 100 * (wide[2] - wide[1]) / wide[1]

    # Mean effect and 95% CI on the mean
    mean = effect.mean()
    ci = 1.96 * effect.sem()

    for ax, par in zip(axes, params):
        ax.errorbar(mean[par], drug, xerr=ci[par], fmt='o',
                    color=effect_color(mean[par], ci[par]))

# Legend (proxy handles instead of dummy out-of-range points)
legend = [Line2D([], [], marker='o', ls='', color=c, label=label)
          for c, label in [('tab:red', 'inhibition > 20%'),
                           ('tab:orange', 'inhibition'),
                           ('tab:green', 'no inhibition')]]
axes[1].legend(handles=legend, loc='center left', bbox_to_anchor=(1, 0.5))

plt.show()

# %%
# Discussion
# ----------
# These results confirm the key findings from the paper: 
# 
# - Two of the tested drugs (rifampicin and cyclosporine) showed 
#   strong inhibition of both uptake and excretion. 
# - One drug (ketoconazole) inhibits uptake but not excretion. 
# - Three drugs (pioglitazone, bosentan and asunaprevir) inhibit 
#   excretion but not uptake.

# sphinx_gallery_start_ignore
# Choose the last image as a thumbnail for the gallery
# sphinx_gallery_thumbnail_number = -1
# sphinx_gallery_end_ignore
