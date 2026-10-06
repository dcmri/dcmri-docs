"""
==========================================================
Clinical - rifampicin induced inhibition of liver function
==========================================================

This example illustrates the use of `~dcmri.AortaLiver2scan` for joint 
fitting of aorta and liver signals measured over 2 separate scans. The use 
case is provided by the liver work package of the 
`TRISTAN project <https://www.imi-tristan.eu/liver>`_  which develops imaging 
biomarkers for drug safety assessment. The data and analysis was first 
presented at the ISMRM in 2024 (Min et al 2024, manuscript in press). 

The data were acquired in the aorta and liver of 10 healthy volunteers with 
dynamic gadoxetate-enhanced MRI, before and after administration of a drug 
(rifampicin) which is known to inhibit liver function. The assessments were 
done on two separate visits at least 2 weeks apart. On each visit, the 
volunteer had two scans each with a separate contrast agent injection of a 
quarter dose each. the scans were separated by a gap of about 1 hour to enable 
gadoxetate to clear from the liver. This design was deemed necessary for 
reliable measurement of excretion rate when liver function was inhibited.

The research question was to what extent rifampicin inhibits gadoxetate uptake 
rate from the extracellular space into the liver hepatocytes 
(khe, mL/min/100mL) and excretion rate from hepatocytes to bile 
(kbh, mL/100mL/min). 

2 of the volunteers only had the baseline assessment, the other 8 volunteers 
completed the full study. The results showed consistent and strong inhibition 
of khe (95%) and kbh (40%) by rifampicin. This implies that rifampicin poses 
a risk of drug-drug interactions (DDI), meaning it can cause another drug to 
circulate in the body for far longer than expected, potentially causing harm 
or raising a need for dose adjustment.

**Note**: this example is different to the 1 scan example of the same study in 
that this uses both scans to fit the model. 

Reference
--------- 

Thazin Min, Marta Tibiletti, Paul Hockings, Aleksandra Galetin, Ebony Gunwhy, 
Gerry Kenna, Nicola Melillo, Geoff JM Parker, Gunnar Schuetz, Daniel Scotcher, 
John Waterton, Ian Rowe, and Steven Sourbron. *Measurement of liver function 
with dynamic gadoxetate-enhanced MRI: a validation study in healthy 
volunteers*. Proc Intl Soc Mag Reson Med, Singapore 2024.
"""

# %%
# Setup
# -----

# Import packages
import pandas as pd
import matplotlib.pyplot as plt
import pydmr
import dcmri as dc

# Fetch the data from the TRISTAN rifampicin study:
dmrfile = dc.fetch('tristan_humans_healthy_rifampicin')
data = pydmr.read(dmrfile, 'nest')
rois, pars = data['rois'], data['pars']

# %%
# Model definition
# ----------------
# In order to avoid some repetition in this script, we define a function that 
# returns a trained model for a single dataset with 2 scans:

def tristan_human(roi, par, **kwargs):

    # --- Get the time arrays to find the maximum time
    time_1 = roi['time_1'] - roi['time_1'][0]
    time_2 = roi['time_2'] - roi['time_1'][0]

    # --- Initialise the model with known defaults
    model = dc.AortaLiverDynamic(

        # Configuration
        kinetics = '1I-IC',
        sequence = '3D-SPGR-SS',
        non_stationary = 'U',

        # Indicator
        agent = 'gadoxetate',
        dose_1 = par['dose_1'],
        dose_2 = par['dose_2'],
        rate = 1,

        # Signal
        FA = par['FA_1'],
        FA_2 = par['FA_2'],
        field_strength = 3,
        t_scan2 = time_2[0],
        TR = par['TR'],
        TS = time_1[1],

        # Electromagnetic
        R10_a = 1/par['T1_aorta_1'],
        R10_l = 1/par['T1_liver_1'],

        # Physiological
        weight = par['weight'],
        vol_l = par['liver_volume'],

        # Hyperparameter
        tmax = max(time_2),
    )

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
    
    R102a, R102l = 1/par['T1_aorta_3'], 1/par['T1_liver_3']
    _, sdev, _ = model.train(time, signal, R102a=R102a, R102l=R102l, n0=n0, **kwargs)

    # Export the numerical parameters, including derived
    pars = model.export_params(sdev=sdev, group='phys', deriv=True)

    # Return as dataframe
    df = pd.DataFrame.from_dict(pars, orient='index')
    return df.reset_index().rename(columns={'index': 'parameter'})


# %%
# Fit all data
# ------------
# Now that we have illustrated an individual result in some detail, we 
# proceed with fitting the data for all 10 volunteers, at baseline and 
# rifampicin visit. We do not print output for these individual computations 
# and instead store results in one single dataframe:

results = []

# Loop over all datasets
for subj in rois.keys():
    for visit in rois[subj].keys():

        roi = rois[subj][visit]
        par = pars[subj][visit]

        # Generate a trained model for the scan:
        df = tristan_human(roi, par, xtol=1e-3)

        # Add visit and subject info
        df['subject'] = subj
        df['visit'] = visit

        # Add to the list of all results
        results.append(df)

# Combine all results into a single dataframe
results = pd.concat(results).reset_index(drop=True)

# Print all results
print(results.to_string())


# %%
# Plot individual results
# -----------------------
# Now lets visualise the main results from the study by plotting the drug 
# effect for all volunteers, and for both biomarkers: uptake rate ``khe`` 
# and excretion rate ``kbh``:

# Set up the figure
clr = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 
       'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']
fs = 10
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8,3))
fig.subplots_adjust(wspace=0.5)
ax1.set_title('Hepatocellular uptake rate', fontsize=fs, pad=10)
ax1.set_ylabel('khe (mL/min/100mL)', fontsize=fs)
ax1.set_ylim(0, 60)
ax1.tick_params(axis='x', labelsize=fs)
ax1.tick_params(axis='y', labelsize=fs)
ax2.set_title('Biliary excretion rate', fontsize=fs, pad=10)
ax2.set_ylabel('kbh (mL/min/100mL)', fontsize=fs)
ax2.set_ylim(0, 6)
ax2.tick_params(axis='x', labelsize=fs)
ax2.tick_params(axis='y', labelsize=fs)

# Pivot data for both visits to wide format for easy access:
v1 = results[results.visit=='control']
v2 = results[results.visit=='drug']
v1 = v1.pivot(index='subject', columns='parameter', values='value')
v2 = v2.pivot(index='subject', columns='parameter', values='value')

# Plot the rate constants in units of mL/min/100mL
for s in v1.index:
    x = ['baseline']
    khe = [6000 * v1.at[s,'khe']]
    kbh = [6000 * v1.at[s,'kbh']] 
    if s in v2.index:
        x += ['rifampicin']
        khe += [6000 * v2.at[s,'khe']]
        kbh += [6000 * v2.at[s,'kbh']] 
    color = clr[int(s)-1]
    ax1.plot(x, khe, '-', label=s, marker='o', markersize=6, color=color)
    ax2.plot(x, kbh, '-', label=s, marker='o', markersize=6, color=color)
plt.show()

# sphinx_gallery_start_ignore
# Choose the last image as a thumbnail for the gallery
# sphinx_gallery_thumbnail_number = -1
# sphinx_gallery_end_ignore
