"""
=======================
Using library functions
=======================

Fitting models when no end-to-end model is available. 

The most convenient way to fit models to data is to use one of the 
end-to-end models which link parameters directly to data. However, 
when developing new models or exploring new applications, an end-to-end 
model may not yet be available in the package. 

This tutorial shows how dedicated models can be built and applied 
using only library functions. As an example, we will derive 
systemic parameters directly from concentrations measured in the aorta.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import dcmri as dc

# %%
# Data generation
# ---------------
# As data we will use a population-average AIF:

# --- Set timing parameters
dt = 0.1 
tmax = 375
bat = 30

# --- Compute plasma concententration
t = np.arange(0, tmax, dt)
cp_pop = dc.parker(t, BAT=bat)

# %%
# Build a kinetic model
# ---------------------
# Now we build a model from scratch which predicts an aorta plasma 
# concentration from given parameters. We use two library functions, 
# one to parametrise the injection, and one to derive the aorta concentration.

# --- Define the experimental parameters
Hct = 0.45
weight = 70 
agent = 'gadodiamide'
conc = dc.ca_conc(agent)
dose = dc.ca_std_dose(agent)
rate = 3

# --- Define aorta plasma concentration model
def plasma_conc_aorta(t, Eb, Thl, Dhl, To, CO):

    # Injection flux (mmol/sec)
    j_inj = dc.ca_injection(t, weight, conc, dose, rate, bat)

    # Heart-lung system and organs
    hl = ['chain', (Thl, Dhl)]
    orgs = ['comp', (To, )]
    
    # Aorta flux for a heart-lung-organs whole body model
    j_aorta = dc.flux_aorta_hlo(j_inj, dt=dt, E=Eb, heartlung=hl, organs=orgs)

    # Aorta blood concentrations
    c_aorta = j_aorta / CO

    # Aorta plasma concentrations
    c_aorta = c_aorta / (1 - Hct)

    return c_aorta

# %%
# Fit the model
# -------------

# --- Initialise the free parameters using built-in defaults
pars = ['Eb', 'Thl', 'Dhl', 'To', 'CO']
p0 = dc.init(pars).values()
bnds = dc.bounds(pars).values()
lb = [b[0] for b in bnds]
ub = [b[1] for b in bnds]

# --- Perform the fit
vals, _ = curve_fit(plasma_conc_aorta, t, cp_pop, list(p0), bounds=(lb, ub))

# --- Check that this model provides a good description of the population input:
cp_fit = plasma_conc_aorta(t, *vals)

plt.plot(t / 60, 1000 * cp_pop, 'r-', label='Population input')
plt.plot(t / 60, 1000 * cp_fit, 'b-', label='Model fit')
plt.xlabel('Time (min)')
plt.ylabel('Plasma concentration (mM)')
plt.legend()
plt.show()

# %%
# As we can see, the first pass and recirculation are well-described by
# this simple whole body model, though an accurate representation of the second pass 
# would require a more detailed model. 
#
# Let's print the model parameters:
for param, val in zip(pars, vals):
    print(f"{param:<10} : {val}")

# %%
# Note that the cardiac output is high, as is well-known for this AIF model  
# (`Yang et al (2009) <https://onlinelibrary.wiley.com/doi/10.1002/mrm.21912>`_).


# sphinx_gallery_start_ignore
# sphinx_gallery_thumbnail_number = -1
# sphinx_gallery_end_ignore

