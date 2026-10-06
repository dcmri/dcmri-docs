"""
========================================
Single-kidney glomerular filtration rate
========================================

This example illustrates the use of `~dcmri.Kidney` for measurement of 
single-kidney glomerular filtration rate (SK-GFR). 

The script uses data from a validation study comparing MRI-derived 
measurement of SK-GFR against reference measurements performed with 
radio-isotopes (Basak et al 2018). The study used 124 historical 
datasets collected in between the years 2000 and 2010 at 1 Tesla and 
3 Tesla MRI. 

The study was funded by 
`Kidney Research UK <https://www.kidneyresearchuk.org/>`_.

**Reference**

Basak S, Buckley DL, Chrysochou C, Banerji A, Vassallo D, Odudu A, Kalra PA, 
Sourbron SP. Analytical validation of single-kidney glomerular filtration 
rate and split renal function as measured with magnetic resonance renography. 
Magn Reson Imaging. 2019 Jun;59:53-60. doi: 10.1016/j.mri.2019.03.005. 
`[URL] <https://pubmed.ncbi.nlm.nih.gov/30849485/>`_.
"""

# %%
# Setup
# -----

# --- Import packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pydmr
import dcmri as dc

# --- Fetch the data
datafile = dc.fetch('KRUK')
dmr = pydmr.read(datafile, 'nest')
rois, pars = dmr['rois'], dmr['pars']

# %%
# Model definition
# ----------------
# For convenience we define a function that returns a trained model:

def kidney_model(roi, par, kidney):

    # Get B0 and precontrast T1
    B0 = par['field_strength']
    T1 = par[kidney+' T1'] if kidney+' T1' in par else dc.T1(B0, 'kidney')

    # Define tissue model
    model = dc.Kidney(

        # Configuration
        kinetics = '2CF',
        sequence = '3D-SPGR-SS',

        # Indicator quantities
        agent = par['agent'],

        # Signal quantities
        FA = par['FA'],
        field_strength = B0,
        TR = par['TR'],
        
        # Electromagnetic quantities
        R10 = 1 / T1,
    )

    # Train the kidney model on the data
    time, signal = roi['time'], roi[kidney]
    aif = {'signal': roi['aorta'], 'R10': 1/dc.T1(B0, 'blood')}

    model.train(time, signal, aif=aif, n0=par['n0'], bounds={'Tt': [30, 300]})

    return model

# %%
# Fit all data
# ------------
# Now that we have illustrated an individual result in some detail, we proceed 
# to determine SK-GFR for all datasets:

results = []

for subj in rois.keys():
    for visit in rois[subj].keys():
        for kidney in ['LK', 'RK']:

            roi = rois[subj][visit]
            par = pars[subj][visit]
            if kidney not in roi:
                continue
            
            model = kidney_model(roi, par, kidney)

            # Export parameters and add SK-GFR
            params = model.export_params(num_only=True)
            params['iso-SK-GFR'] = {
                'name': 'Isotope single-kidney GFR', 
                'value': par[f'{kidney} iso-SK-GFR'], 
                'unit': 'mL/sec', 
                'sdev': 0,
            }
            params['mrr-SK-GFR'] = {
                'name': 'MRR single-kidney GFR', 
                'value': model.params('Fp') * model.params('FF') * par[kidney+' vol'], 
                'unit': 'mL/sec', 
                'sdev': 0,
            }

            # Convert to a dataframe
            df = pd.DataFrame.from_dict(params, orient = 'index')
            df['participant'] = subj
            df['kidney'] = kidney
            df['visit'] = visit
            df['parameter'] = df.index
            df['B0'] = par['field_strength']

            # Append to results
            results.append(df)

# Combine all results into a single dataframe
results = pd.concat(results).reset_index(drop=True)


# %%
# Plot MRI values and reference values

# --- Separate SK-GFR values
v1T = pd.pivot_table(results[results.B0==1], values='value', columns='parameter', index=['participant','kidney','visit'])
v3T = pd.pivot_table(results[results.B0==3], values='value', columns='parameter', index=['participant','kidney','visit'])

iso1T, iso3T = 60 * v1T['iso-SK-GFR'].values, 60 * v3T['iso-SK-GFR'].values
mri1T, mri3T = 60 * v1T['mrr-SK-GFR'].values, 60 * v3T['mrr-SK-GFR'].values

# --- Plot full range
vmax = np.amax(np.concatenate((iso1T, iso3T, mri1T, mri3T)))

plt.title('Single-kidney GFR (SK-GFR)')
plt.plot(iso1T, mri1T, 'bo', linestyle='None', markersize=4, label='1T')
plt.plot(iso3T, mri3T, 'ro', linestyle='None', markersize=4, label='3T')
plt.plot(iso3T, iso3T, linestyle='-', color='black')
plt.ylabel("MRI SK-GFR (mL/min)")
plt.xlabel("Isotope SK-GFR (mL/min)")
plt.xlim(0, vmax)
plt.ylim(0, vmax)
plt.legend()
plt.show()

# %%
# Plot a detail

vmax = 80

plt.title('Single-kidney GFR (SK-GFR)')
plt.plot(iso1T, mri1T, 'bo', linestyle='None', markersize=4, label='1T')
plt.plot(iso3T, mri3T, 'ro', linestyle='None', markersize=4, label='3T')
plt.plot(iso3T, iso3T, linestyle='-', color='black')
plt.ylabel("MRI SK-GFR (mL/min)")
plt.xlabel("Isotope SK-GFR (mL/min)")
plt.xlim(0, vmax)
plt.ylim(0, vmax)
plt.legend()
plt.show()


# %%
# Compute bias and accuracy

v = pd.pivot_table(results, values='value', columns='parameter', index=['participant','kidney','visit'])

iso = 60 * v['iso-SK-GFR'].values
mri = 60 * v['mrr-SK-GFR'].values

diff = mri-iso
bias = round(np.mean(diff), 0)
bias_err = round(1.96 * np.std(diff) / np.sqrt(np.size(diff)), 0)
err =  round(1.96 * np.std(diff), 0)

print('-----------------')
print('Single-kidney GFR')
print('-----------------')
print(f"The bias in an MRI-based SK-GFR measurement is {bias} +/- {bias_err} ml/min") # paper 0.56
print(f"After bias correction, the error (95% CI) on a single SK-GFR measurement is +/- {err} mL/min") # paper [-28, 29]

# %%
# The results confirm the conclusion from the original study that 
# the precision of MR-derived SK-GFR with these historical data was 
# too low for clinical use. The exact numerical values are different 
# from those in the original study, showing the importance of 
# implementation detail.


# sphinx_gallery_start_ignore
# Choose the last image as a thumbnail for the gallery
# sphinx_gallery_thumbnail_number = -1
# sphinx_gallery_end_ignore

