"""
==============
Inflow effects
==============

What are inflow effects?
------------------------
Inflow effects in the arterial input function (AIF) are a common 
type of artefact in DCE-MRI which severely biases the results if it 
is not properly acccounted for. The effect is caused by unsaturated 
blood flowing into the imaging slab causing an artefactual increase 
of the baseline signal. A naive analysis of inflow-corrupted data 
underestimates the arterial concentration and consequently 
overestimates tissue perfusion parameters. 

Inflow effects can be detected visually by 
inspecting a precontrast image. Since blood has a long T1, arteries 
should be dark on a T1-weighted image. If they are instead 
brighter than surrounding tissue, this is evidence of inflow effects. 
The brightness typically shows a gradient with the vessel being 
brightest at the edge of the slab where flow-induced enhancement is 
most severe, then gradually darking as the blood travels down the slab 
and is pushed into steady-state by the excitation pulses. 

Minimizing inflow effects
-------------------------
The most robust approach to dealing with inflow effects is by 
eliminating them at the source, by optimizing the acquisition. In 
abdominal imaging this can often be achieved by positioning the slab 
coronally and extending the field of view to include the heart. 

This may not always be possible though, for instance for prostate imaging 
where the heart is too far from the region of interest. Even when it 
is technically possible, such as for liver or renal imaging, it may 
require compromises in other areas: the approach forbids axial 
imaging, which is sometimes preferred, and may also come at a cost of 
spatial resolution. 

Other approaches may be possible, such as 
increasing the flip angle to accelerate transition to steady-state; 
but this comes with other compromises such as increased tissue 
heating and reduced signal enhancement.

Correcting inflow effects
-------------------------
If inflow effects cannot be fully avoided by optimizing the 
acquisition, or data with inflow effects are analysed retrospectively, 
the problem must be addressed at image analysis stage. 

One approach 
that has sometimes been applied is to measure the input function 
deeper down in the slab where inflow effects have largely decayed. 
This is not always feasible and may cause variability in result for 
instance due to differences in blood velocity.

This tutorial illustrates two alternative approaches: using a 
standardised input function rather than attempting to measure it; 
and correcting for inflow by adding flow-related enhancement in the 
signal model.

The solutions are illustrated for the use case of MR renography in a 
minipig with unilateral kidney fibrosis. 
"""

# %%
# Setup
# -----

# Import packages
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import dcmri as dc

# Read the dataset
data = dc.load_minipig()

# %%
# Plot data
# ---------
# Let's start by plotting the data:

plt.plot(data['tS_ao'], data['S_ao'], 'r-', label='Aorta')
plt.plot(data['tS_lk'], data['S_lk'], 'g-', label='LeftKidney')
plt.plot(data['tS_rk'], data['S_rk'], 'b-', label='RightKidney')
plt.xlabel('Time (sec)')
plt.ylabel('Signal (a.u.)')
plt.legend()
plt.show()

# %%
# We see a clear difference between left kidney (healthy) and right 
# kidney (fibrotic). We also 
# see that the peak signal change in the aorta is similar to that in 
# the kidney. As peak aorta concentrations in pure blood are always 
# substantially higher than those in tissue, this shows that 
# signal changes underestimate concentrations - consistent with the 
# effect of inflow artefacts.
# 
# Verification on the data confirms this suspicion: looking at a 
# precontrast slice through the aorta (below) we see that the aorta 
# is bright compared to the surrounding tissue, and gradually becomes 
# darker as we move further down into the slab - this is the signature 
# sign of inflow artefacts. 

img = mpimg.imread('../../source/_static/tutorial-inflow.png')
plt.figure(figsize=(6, 4))
plt.imshow(img)
plt.axis("off")
plt.title("Baseline image")
plt.show()


# %%
# Standard analysis
# -----------------
# Ignoring the inflow effects leads to significant bias in the 
# results. For the kidney 
# the most common modelling approach is implemented in the function 
# `dcmri.Kidney`. Let's run it on the left kidney and see what we get:

kidney = dc.InverseKidney(
    # TODO: imap does not work here because popt is not mapped in return
    # Need to map popt everywhere before returning
    # TODO: pfree need mapping to if provided at input
    kinetics='2CF',
    sequence='ZTE-3D-SPGR-SS', 
    t2s_relaxation=None, # TODO: This is pointless. Ignor T2s-relaxation instead
    aif='measured',
)
data |= {
    'tS_ki': data['tS_lk'], 
    'S_ki': data['S_lk']
}
result = kidney(data) 
# # TODO: Remove **kwargs option in call for data in __call__ - kwargs 
# # for genuine kwargs that are not input parameters
# # Calling this with kwargs would cause plot to fail.
# # One way of calling better than allowing two ways

kidney.plot(data, result)

# %%
dc.print_quantities(result['popt'], digits=2)

# %%
# The model is not fitting the data because by default the model 
# parameters are not allowed to enter into unphysical regimes. So 
# the model stops converging when they hit their bounds, as 
# can be seen from the plasma flow which converged to its upper 
# bound of 1.0 mL/sec/cm3. 

# %%
# If we free up the parameters then the model will fit a lot better, albeit
# with unphysical values for the parameters:

data['pfree'] = kidney.pfree() | {
    'F_p_ki':[0, 1],  
    'v_p_ki': [0, 1], 
}

result = kidney(data)
kidney.plot(data, result)

# %%
dc.print_quantities(result['popt'], digits=2)

# %%
# The plasma flow and volume now hit the ceiling of what is allowed,  
# many times higher than typical values in tissue - confirming the 
# massive bias caused by inflow artefacts. 

# %%
# Using a standard input function
# -------------------------------
# One approach that can always be considered if arterial 
# concentrations are not reliable is to use a modelled rather than a 
# measured input function. 

kidney = dc.InverseKidney(
    kinetics='2CF',
    sequence='ZTE-3D-SPGR-SS', 
    t2s_relaxation=None,
    aif='fixed',
)

# %%
# There are no input function models available for minipigs so 
# our best option is to use one derived for humans and adjust the 
# parameters. We will use the function `dcmri.aif_tristan` which is 
# built on a model of the circulation and thefore defined in terms 
# of physiological parameters. 
# 
# We set the cardiac output (CO) to a typical value for the 
# minipig (3.6 L/min or 60 mL/sec). The bolus arrival time (BAT) can 
# be estimated from the 
# peak of the aorta concentration - it does not have to be exact as the 
# value is optimized in the fit. All other parameters are left at 
# default values as no data exist for the minipig:

dt = 0.25
t = np.arange(0, np.amax(data['tS_ao']) + 10, dt)  
ca = dc.tristan(t, # TODO Build dc.AifTristan() and rename dc.Parker() to dc.AifParker()
    agent="gadoterate",
    dose=data['dose'],
    rate=data['rate'],
    weight=data['weight'],
    CO=60,
    BAT=data['tS_ao'][np.argmax(data['S_ao'])] - 20,
)

# %%
# Now we can use this fixed concentration as input in the kidney 
# model instead of the measured aorta signal.

data['dt'] = dt
data['c_ar'] = ca / (1 - 0.45) # TODO: Blood vs plasma needs a consistent approach. Should be always blood at this level

result = kidney(data)
kidney.plot(data, result)

# %%
dc.print_quantities(result['popt'], digits=2)

# %%
# This now fits a lot better without unphysical parameter values, 
# but the fit remains poor - indicating the input function does not 
# represent reality very well even after adapting the parameters.

# %%
# Model-based inflow correction
# -----------------------------
# An alternative solution is to fit an 
# aorta model to the data and use a signal model that 
# accounts for inflow effects (`tof_corr=True`). 
# 
# The CO is set to the same values as for the modelled AIF above, 
# but here this serves as initial guess rather than a fixed 
# parameter:

aorta = dc.InverseAorta(
    heartlung='chain', 
    organs='2cxm', 
    baseline='measured',
    tof_corr=False,
    sequence='ZTE-3D-SPGR-SS', 
    t2s_relaxation=None,
)

# missing_data = aorta.inputs() - data.keys()
# dc.print_quantities(missing_data)

data.pop('pfree') # TODO fails because some pfree not model params - not consistent. function shoudld just ignore invalid pfree parameters
data['tS'] = data['tS_ao'] # TODO not consistent - aorta should take named inputs like the others
data['S'] = data['S_ao']

result = aorta(data)
aorta.plot(data, result)

# %%
dc.print_quantities(result['popt'])

# %%
# This fits the signals well but produces unphysical CO at the ceiling of 500 mL/sec. 
# Let's try this again, but this time with inflow correction:

aorta = dc.InverseAorta(
    heartlung='chain', 
    organs='comp', 
    baseline='measured',
    tof_corr=True,
    sequence='ZTE-3D-SPGR-SS', 
    t2s_relaxation=None,
)
result = aorta(data)

aorta.plot(data, result)

# %%
dc.print_quantities(result['popt'])

# %%
# This produces a good fit to the data and also reasonable 
# values for the parameters. A cardiac output of 74 mL/sec 
# equates to 4.5 L/min, which is in the right range for a minipig. 
# Also a travel time of 280 msec (Inflow time) from heart to renal arteries 
# seems reasonable. The peak concentrations (right) are also in the 
# expected range for a standard injection (6mM). 

# %%
# Kidney model
# ------------
# We can now use the output from the aorta model to generate 
# concentrations and use those as input for the kidney model, 
# instead of the modelled concentration:

pred = aorta.predict(data, result)
data['c_ar'] = pred['C'][0,:] / (1 - 0.45)

result = kidney(data)
kidney.plot(data, result)

# %%
dc.print_quantities(result['pars'], digits=2, title='Functional kidney (left)')



# %%
# This now gives a good fit with reasonable values for all parameters. 
# Let's run it on the right kidney as well so we can compare 
# parameters:

data |= {
    'tS_ki': data['tS_rk'], 
    'S_ki': data['S_rk']
}

result = kidney(data)
kidney.plot(data, result)

# %%
dc.print_quantities(result['pars'], digits=2, title='Fibrotic kidney (right)')

# %%
# The right (fibrotic) kidney now shows a substantially lower 
# perfusion and function than the left. The perfusion of the left 
# kidney has not hit the maximum value. It is still relatively high 
# (Fp = 0.033 mL/sec/cm3 or 198 mL/min/100mL) but it is possible 
# that it is overcompensating to some extent for the damage on the 
# right kidney.


# %%
# Joint aorta-kidneys fit
# -----------------------
# The method above produces a good solution for these data, but if the 
# volumes of the kidneys are known this can be further refined 
# by performing a joint fit of aorta and both kidneys. 
# 
# This is not only more compact but should also be more robust 
# as shared parameters can be eliminated and all data are accounted 
# for equally. In this example the volumes are not actually known, 
# so for the purpose of illustration we use a typical value of 
# 85mL (note the kidneys are unlikely to be symmetric so this causes a 
# bias in the left-right comparison of parameters such as GFR): 

data |= {'vol_lk': 85, 'vol_rk': 85}

aorta_kidneys = dc.InverseAortaKidneys(
    heartlung='chain',          # Smoother first pass data
    organs='2cxm',              # Long acquisition times reveal extravasation # TODO to upper case 2CX for consistency
    kidneys='2CF',              # Intracellular agent
    baseline='measured',        # Data are available on precontrast T1
    tof_corr=True,
    sequence='ZTE-3D-SPGR-SS',
    t2s_relaxation_ao=None,     # No T2* relaxation with TE=0
    t2s_relaxation_lk=None,     # No T2* relaxation with TE=0
    t2s_relaxation_rk=None,     # No T2* relaxation with TE=0 # TODO relaxation models are always the same for left and right. Needs just on t2s_relaxation_ki
)

result = aorta_kidneys(data)
aorta_kidneys.plot(data, result)

# %%
dc.print_quantities(result['popt'] | result['pars'], digits=3, title='Joint Aorta-Kidneys fit')

# %%
# This produces all results for aorta and kidneys in one go, which 
# also allows to derive some secondary parameters such as 
# differential function which would otherwise have to be computed 
# from separate results. Since the model uses the volumes this can 
# also automatically output important whole kidney parameters such 
# as GFR and RPF. Numerically the values are similar - though not 
# identical - to those produced from a separate Aorta and Kidneys fit.

# sphinx_gallery_start_ignore
# sphinx_gallery_thumbnail_number = -1
# sphinx_gallery_end_ignore