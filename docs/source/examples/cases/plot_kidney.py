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
import dcmri as dc

# %%
# Identify a configuration
# ------------------------
# We'll use a 2-compartment filtration model for the kidney and 
# assume acquisition with a 3D-SPGR-SS sequence:

kidney = dc.InverseKidney(
    sequence='ZTE-3D-SPGR-SS', 
    t2s_relaxation=None, 
    calibrate=True,
    aif='measured',
)

# %%
# Let's see what input parameters are needed for this model:

kidney.print_inputs()

def get_data(subject, kid, visit):
    data = dc.load_kruk(subject, kid, visit)
    data['pfree'] = kidney.pfree() | {'T_u': [30, 300]}
    return data

# --- The dataset to be analysed
data = get_data('001', 'LK', 'pre')


# %%
# Train the Kidney model
# ----------------------
# --- Train the kidney model on the data
result = kidney(data)

# --- Update data
data |= result['popt'] | {'c_ar': result['c_ar']}

# --- Plot the results to check that the model has fitted the data
kidney.plot(data)

# %%
# Numerical results
# -----------------
# Print the measured model parameters:
dc.print_quantities(result, digits=2)

#%%
# Compare the measured SK-GFR to the 
# radio-isotope reference value:

mrr_sk_gfr = data['FF'] * data['F_p_ki'] * data['vol_ki']
iso_sk_gfr = data['GFR']

print(f"Radio-isotope SK-GFR: {round(60 * iso_sk_gfr)} mL/min")
print(f"MRR SK-GFR: {round(60 * mrr_sk_gfr)} mL/min")


# sphinx_gallery_start_ignore
# Choose the last image as a thumbnail for the gallery
# sphinx_gallery_thumbnail_number = -1
# sphinx_gallery_end_ignore

