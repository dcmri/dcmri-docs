"""
=====
Aorta
=====

This tutorial will illustrate the use of a simple whole-body model 
`~dcmri.Aorta` in the measurement of cardiac output from an 
arterial input function (AIF). 

An arterial input function (AIF) is traditionally used in DC-MRI to 
derive an input concentration to a tissue model, which can then be 
used to estimate tissue properties such as blood flow and permeability.

Typically, a signal is measured in the aorta or a large artery, and 
this is converted analytically to aorta concentrations. An analytical 
inversion is sometimes problematic due to the high concentrations in 
aorta, which may cause the signal to reach a ceiling where it is 
no longer reflective of further changes in concentration. The signal is 
then not invertible, and any attempt to do so may lead to extreme 
values for the concentrations.

An alternative approach is to model the AIF directly and then derive the 
concentrations by fitting the model parameters directly to the signal, 
rather than performung a direct analytical inversion. This may 
provide more reasonable results in cases where the signal is not invertible, 
and also produces additional model parameters that may have some utility.

Here we use this approach to measure the cardiac output of 
subjects from a literature-based input function. 
A popular choice is the AIF derived by 
`Parker et al (2006) <https://onlinelibrary.wiley.com/doi/full/10.1002/mrm.21066>`_, 
which is implemented in `dcmri` as the function `~dcmri.parker`. 

As a model we will use `~dcmri.Aorta`, a whole-body model that can be used 
to model input functions, derive arterial concentrations without the need 
for explicit inversion, and derive systemic parameters such as cardiac output.
"""

import numpy as np
import matplotlib.pyplot as plt
import dcmri as dc


# %%
# Generate the data
# -----------------
# We first define the required constants:

dt = 0.1 
tmax = 375
bat = 30
Hct = 0.45 # Estimate - not provided in the original paper
B0 = 1.5
R1b = 1 / dc.T1(B0, 'blood')
R2sb = 1 / 0.2 
r1 = dc.r1(B0, 'blood', 'gadodiamide') 
r2s = dc.r2s(B0, 'blood', 'gadodiamide')
FA = 20
TR = 0.004
TE = 0.00082
S0 = 100 # This is arbitrary

# %%
# The `~dcmri.Aorta` model predicts signals. The paper only provides 
# the concentrations so we need to derive the signal:

# --- Compute plasma concententration
t = np.arange(0, tmax, dt)
cp_pop = dc.parker(t, BAT=bat)

# --- Convert to blood concentration
cb_pop = (1 - Hct) * cp_pop    

# --- Convert to relaxation rates
R1 = R1b + r1 * cb_pop
R2s = R2sb + r2s * cb_pop

# --- Convert to signal
sig_pop = dc.Signal('3D-SPGR-SS')(S0=S0, R1=R1, R2s=R2s, TR=TR, FA=FA, TE=TE)

# %%
# Set up the Aorta model
# ----------------------
# First we need to decide how to configure the model, so let's 
# see what options are available:

dc.Aorta.print_configs()

# %%
# Let's choose a chain model for the heart-lung system 
# and a single compartment for the organs. The acquisition is done 
# with a 3D-SPGR sequence in steady-state, so the configuration becomes:

config = {
    'heartlung': 'chain',
    'organs': 'comp',
    'sequence': '3D-SPGR-SS'
}

# %%
# Next we need to set suitable values for the constant parameters, 
# so lets print out the default state for this configuration: 

dc.Aorta(**config).print_params(round_to=3)

# %%
# Initialise an aorta model with the experimental parameters set to the 
# correct values:
aorta = dc.Aorta(
    agent='gadodiamide',
    dose=0.2, 
    dt=dt, 
    FA=FA, 
    field_strength=B0, 
    rate=3,
    R10_a=R1b, 
    R20s_a=R2sb, 
    TE=TE,
    TR=TR, 
    weight=70, 
    **config
)

# %%
# Train the Aorta model
# ---------------------
# Train the model using the population AIF, and check that it fits the data:

aorta.train(t, sig_pop)
aorta.plot(t, sig_pop)

# %%
# We can also check that the concentrations derived from the trained 
# model provide a good approximation to the actual concentrations:
plt.plot(t / 60, 1000 * cp_pop, 'r-', label='Actual ')
plt.plot(aorta.time() / 60, 1000 * aorta.conc() / (1 - Hct), 'b-', label='Reconstructed')
plt.xlabel('Time (min)')
plt.ylabel('Plasma concentration (mM)')
plt.legend()
plt.show()

# %%
# Check the kinetic model parameters after training
aorta.print_params('Eb', 'Thl', 'Dhl', 'To', 'CO', round_to=2)

# %%
# These are all values in an expected range, except for the cardiac 
# output which is high: A value of 226 mL/sec corresponds to 13.5 L/min, 
# which is more than double of typical values in healthy volunteers. 
# This has been observed before by 
# `Yang et al (2009) <https://onlinelibrary.wiley.com/doi/10.1002/mrm.21912>`_,
# though their estimate was less elevated (10.5 L/min). 


# sphinx_gallery_start_ignore
# sphinx_gallery_thumbnail_number = -1
# sphinx_gallery_end_ignore

