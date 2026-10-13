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
    heartlung='chain',         # Smoother first pass data
    organs='comp',              # Long acquisition times reveal extravasation
    kidneys='2CFU',              # Intracellular agent
    baseline='measured',        # Data are available on precontrast T1
    sequence='ZTE-3D-SPGR-SS',
    # tof_corr=True,
    # sequence='ZTE-3D-SPGR-SS',  # Echo times are assumed to be zero
    t2s_relaxation_ao=None,     # No T2* relaxation with TE=0
    t2s_relaxation_lk=None,     # No T2* relaxation with TE=0
    t2s_relaxation_rk=None,     # No T2* relaxation with TE=0
    calibrate=True,             # Derive signal scaling factor from data
    estimate_bat='custom',      # Use the dedicated BAT estimator
)

#aok.print_inputs()

data = dc.load_kruk('001', 'pre')

dc.print_quantities(data)

result = aok(data, verbose=2)

# Export SK-GFR and check against reference
p = data | result['popt']
RPF = (1 - p['H']) * p['fCO_ki'] * p['CO']
GFR_lk = p['FF_lk'] * p['DRPF'] * RPF
GFR_rk = p['FF_rk'] * (1 - p['DRPF']) * RPF

iso_lk, iso_rk = round(60 * p['nmGFR_lk']), round(60 * p['nmGFR_rk'])
mrr_lk, mrr_rk = round(60 * GFR_lk), round(60 * GFR_rk)

print(f"{'GFR (mL/min)':<14}{'Radio-isotope':>15}{'MRR':>8}")
print("-" * 37)
print(f"{'Left kidney':<14}{iso_lk:>15}{mrr_lk:>8}")
print(f"{'Right kidney':<14}{iso_rk:>15}{mrr_rk:>8}")

aok.plot(data, result)

# sphinx_gallery_start_ignore
# sphinx_gallery_thumbnail_number = -1
# sphinx_gallery_end_ignore