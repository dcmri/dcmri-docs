"""
============
AortaKidneys
============

These example shows the use of the `~dcmri.AortaKidneys` model to 
fit signals measured in aorta and both kidneys simultaneously. 
"""

# %%
# Import packages
# ---------------
import dcmri as dc

# %%
# Set up the model
# ----------------
aok = dc.InverseAortaKidneys(
    heartlung='chain',          # Smoother first pass data
    organs='2cxm',              # Long acquisition times reveal extravasation # TODO to upper case 2CX for consistency
    kidneys='2CF',              # Intracellular agent
    # veins='plug',
    baseline='measured',        # Data are available on precontrast T1
    sequence='ZTE-3D-SPGR-SS',
    t2s_relaxation_ao=None,     # No T2* relaxation with TE=0
    t2s_relaxation_lk=None,     # No T2* relaxation with TE=0
    t2s_relaxation_rk=None,     # No T2* relaxation with TE=0 # TODO relaxation models are always the same for left and right. Needs just on t2s_relaxation_ki
    estimate_bat='custom',      # Use the dedicated BAT estimator
)

#aok.print_inputs()

#data = dc.load_kruk('061', 'pre')
data = dc.load_kruk('008', 'pre')

result = aok(data, verbose=2)

# %%

p = data | result['popt'] | result['pder']

dc.print_quantities(result['popt'] | result['pder'], digits=3)

# %%

iso_lk, iso_rk = round(60 * p['nmGFR_lk']), round(60 * p['nmGFR_rk'])
mrr_lk, mrr_rk = round(60 * p['GFR_lk']), round(60 * p['GFR_rk'])

print(f"{'GFR (mL/min)':<14}{'Radio-isotope':>15}{'MRR':>8}")
print("-" * 37)
print(f"{'Left kidney':<14}{iso_lk:>15}{mrr_lk:>8}")
print(f"{'Right kidney':<14}{iso_rk:>15}{mrr_rk:>8}")

# %%
aok.plot(data, result, xlim=None)

# sphinx_gallery_start_ignore
# sphinx_gallery_thumbnail_number = -1
# sphinx_gallery_end_ignore