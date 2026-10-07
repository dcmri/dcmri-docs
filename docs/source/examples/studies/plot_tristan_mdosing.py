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
data_file = dc.fetch('tristan_rats_healthy_multiple_dosing')
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
# Now let's plot the biomarker values across visits for each study group.
# For this exercise, let's specify Ktrans and kbh as the biomarker parameters that
# we are interested in. For each subject, we can visualise the change in
# biomarker values between visits. For reference, in the below plots, the
# studies are numbered as follows:
# Study 1: Rifampicin repetitive dosing regime
# Study 2: Cyclosporine repetitive dosing regime
# Study 3: Bosentan repetitive dosing regime

import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams.update({
    'axes.titlesize': 25, 'axes.labelsize': 20,
    'axes.labelweight': 'bold', 'axes.titleweight': 'bold',
    'font.weight': 'bold',
    'axes.linewidth': 1.5,
    'xtick.labelsize': 15, 'ytick.labelsize': 15,
    'lines.linewidth': 1.5, 'lines.markersize': 2,
})

# parameter -> y-axis limits, in row order (top to bottom)
rows = {'k_e2h': (0, 300), 'k_h2b': (0, 30)}

# Rate constants in units of mL/min/100cm3
data = (results[results.parameter.isin(list(rows))]
        .assign(value=lambda d: 6000 * d['value']))

g = sns.catplot(data=data,
                x='visit', y='value',
                hue='subject', palette='rocket',
                row='parameter', row_order=list(rows),
                col='study',
                kind='point',
                sharey='row',
                legend=False)

# One title per column, on the top row only
g.set_titles("")
for ax, study in zip(g.axes[0], g.col_names):
    ax.set_title(f"Study {study}", pad=15)

# One y-axis label and one set of limits per row
for ax_row, (par, ylim) in zip(g.axes, rows.items()):
    ax_row[0].set_ylabel(f"{par} [mL/min/100cm3]")
    ax_row[0].set_ylim(ylim)

plt.tight_layout()
plt.show()


# Choose the last image as a thumbnail for the gallery
# sphinx_gallery_thumbnail_number = -1
