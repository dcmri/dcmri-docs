"""
======================================================
Preclinical - effect on liver function of 6 test drugs
======================================================

This example illustrates the use of `~dcmri.Liver` for fitting of signals 
measured in liver. The use case is provided by the liver work package of the 
`TRISTAN project <https://www.imi-tristan.eu/liver>`_  which develops imaging 
biomarkers for drug safety assessment. The data and analysis were first 
published in Melillo et al (2023). 

The specific objective of the study was to determine the effect of selected 
drugs on hepatocellular uptake and excretion of the liver-specific contrast 
agent gadoxetate. If a drug inhibits uptake into liver cells, then it might 
cause other drugs to circulate in the blood stream for longer than expected, 
potentially causing harm to other organs. Alternatively, if a drug inhibits 
excretion from the liver, then it might cause other drugs to pool in liver 
cells for much longer than expected, potentially causing liver injury. These 
so-called drug-drug interactions (DDI's) pose a significant risk to patients 
and trial participants. A direct in-vivo measurement of drug effects on liver 
uptake and excretion can potentially help improve predictions of DDI's and 
inform dose setting strategies to reduce the risk.

The study presented here measured gadoxetate uptake and excretion in healthy 
rats before and after injection of 6 test drugs. Studies were performed in 
preclinical MRI scanners at 3 different centers and 2 different field 
strengths. Results demonstrated that two of the tested drugs (rifampicin and 
cyclosporine) showed strong inhibition of both uptake and excretion. One drug 
(ketoconazole) inhibited uptake but not excretion. Three drugs (pioglitazone, 
bosentan and asunaprevir) inhibited excretion but not uptake. 

**Reference**

Melillo N, Scotcher D, Kenna JG, Green C, Hines CDG, Laitinen I, Hockings PD, 
Ogungbenro K, Gunwhy ER, Sourbron S, et al. Use of In Vivo Imaging and 
Physiologically-Based Kinetic Modelling to Predict Hepatic Transporter 
Mediated Drug–Drug Interactions in Rats. Pharmaceutics. 2023; 15(3):896. 
`[DOI] <https://doi.org/10.3390/pharmaceutics15030896>`_ 
"""

# %%
# Setup
# -----

# --- Import packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pydmr
import dcmri as dc

# --- Fetch the data
dmrfile = dc.fetch('tristan_rats_healthy_six_drugs')
dmr = pydmr.read(dmrfile, 'nest')
rois, pars = dmr['rois'], dmr['pars']


# %%
# Model definition
# ----------------
# See case study

def liver_data(subject, visit):

    # --- Get the data for the subject and visit
    roi = dmr['rois'][subject][visit]
    par = dmr['pars'][subject][visit]

    # --- Generate the input function 
    dt = 0.5
    bat = par['BAT'] + roi['time'][1] / 2
    t = np.arange(0, np.amax(roi['time']) + 180, dt)
    ca = dc.tristan_rat(t, BAT=bat, duration=par['duration'])

    # Acquisition is retrospectively triggered so Nph can be derived
    ts = roi['time'][1] - roi['time'][0]
    Nph = int(np.round(ts / par['TR'])) 

    # --- Create a data dictionary with values for all inputs
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
        'F_p_li': 0.022,      # doi: 10.1021/acs.molpharmaceut.1c00206
        'H': 0.418,           # Cremer et al, J Cereb Blood Flow Metab 3, 254-256 (1983)
        'v_e_li': 0.23,
        'v_li': 1.0,
        'pfree': {'k_e2h':[0, 1], 'T_h': [0, 60 * 60]},
    }


# %%
# Fit all data
# ------------

liver = dc.InverseLiver(kinetics='1I-IC-HF', calibrate=True)

records = []
for subj, visits in rois.items():
    for visit in visits:
        inputs = liver_data(subj, visit)
        result = liver(inputs) 
        data = dmr['pars'][subj][visit]

        for parameter, value in result['pder'].items():
            records.append({
                'subject': subj,
                'study': data['study'],
                'visit': data['visit'],
                'parameter': parameter,
                'value': value,
            })

# %%
# For analysis, save the result as a data table in long format
results = pd.DataFrame(records)
print(results.to_string())


# %%
# Plot individual results
# -----------------------
# Now lets visualise the main results from the study by plotting the drug 
# effect for all rats, and for both biomarkers: uptake rate ``k_e2h`` and 
# excretion rate ``k_h2b``:

clr = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown']
fs = 10
scale = 6000  # rate constants in mL/min/100mL

studies = {5: 'Asunaprevir', 10: 'Bosentan', 8: 'Cyclosporine',
           7: 'Ketoconazole', 6: 'Pioglitazone', 12: 'Rifampicin'}
rows = [('k_e2h', 300), ('k_h2b', 30)]   # (parameter, y-axis maximum)

fig, ax = plt.subplots(len(rows), len(studies), figsize=(9, 8), sharey='row')
fig.subplots_adjust(wspace=0.2, hspace=0.1)

for col, (study, drug) in enumerate(studies.items()):
    ax[0, col].set_title(drug, fontsize=fs, pad=10)
    data = results[results.study == study]

    for row, (par, _) in enumerate(rows):
        # subjects x visits table for this parameter
        vals = (data[data.parameter == par]
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
# Plot effect sizes
# -----------------
# Now lets calculate the effect sizes (relative change) for each drug, along 
# with 95% confidence interval, and show these in a plot. Results are 
# presented in **red** if inhibition is more than 20% (i.e. upper value of 
# the 95% CI is less than -20%), in **orange** if inhbition is less than 20% 
# (i.e. upper value of the 95% CI is less than 0%), and in **green** if no 
# inhibition was detected with 95% confidence (0% in the 95% CI):

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
    data = results[results.study == study]

    # One pivot for both visits: columns are (visit, parameter)
    wide = data.pivot_table(index='subject', columns=['visit', 'parameter'],
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

# sphinx_gallery_start_ignore
# Choose the last image as a thumbnail for the gallery
# sphinx_gallery_thumbnail_number = -1
# sphinx_gallery_end_ignore
