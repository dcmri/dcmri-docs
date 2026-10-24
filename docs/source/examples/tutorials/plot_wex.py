"""
==============
Water exchange
==============

This tutorial will explore the effect of water exchange in a standard 
two-compartmental tissue using the models in `dcmri.Tissue`.

The three tissue compartments involved are the blood, interstitium and tissue 
cells. The water exchange effects refer to the transport of water across the 
barriers between them: **transendothelial** water exchange between blood and 
interstitium, and **transcytolemmal** water exchange between interstitium and 
tissue cells. The water exchange in the blood compartment between plasma and 
red blood cells is assumed to be in the fast exchange limit. 

Water exchange across either of these two barriers can be in the 
fast-exchange limit (F), restricted (R), or there may be no water exchange at 
all (N). Since there are two barriers involved this leads to 3x3=9 possible 
water exchange regimes. `dcmri.Tissue` denotes these 9 regimes by a 
combination of the letters F, R and N: the frst letter refers to the water 
exchange across the endothelium, and the second to the water exchange across 
the cell wall. For instance, 'FR' means fast water exchange (F) across the 
endothelium, and restricted water exchange (R) across the cell wall.

For regimes with restricted water exchange, the rate of exchange is quantified 
by the permeability-surface area (PS) of water, a quantity in units 
of mL/sec/cm3. `dcmri.Tissue` uses the notation ``PSe`` for the 
transendothelial water PS and ``PSc`` for the transcytolemmal PS.
"""

# %%
# Simulation setup
# ----------------
# We set up the simulation by importing the necessary packages and defining 
# the constants that will be fixed throughout. 

# %%
import numpy as np
import matplotlib.pyplot as plt
import dcmri as dc

# Generate a synthetic AIF with default settings
aif = dc.Parker()()

# Store input concentration as c_ar
aif['c_ar'] = aif['C'] # TODO rename 'C' - to'C_ao' in Parker()?

# %% 
# The role of water exchange
# ----------------------------
# To show how water exchange is relevant in DC-MRI analysis, it is insightful 
# to first consider the extreme ends of the water exchange spectrum in some 
# more detail: fast water exchange (F) and no water exchange (N). 
# 
# Let's first generate a tissue without water exchange across either barrier:

tissue_nn = dc.ForwardTissueX(water_exchange='NN') # TODO remove Forward from name, keep only inverse
tissue_nn.plot(aif)

# %%
# In this model the indicator and water occupy the same compartments, so the 
# concentrations on the right have a similar profile. The magnetization (bottom left) 
# follows the profile of the indicator concentrations exactly: since 
# magnetization cannot 
# exchange, it cannot equilibrate and remains directly proportional to the 
# concentration in the compartment. Notably, the magnetization in the tissue 
# cells remains constant as no indicator can enter this 
# compartment to modify it, and no magnetization can be transferred.
# 
# Now lets consider the opposite scenario of fast water exchange across both 
# barriers (*Note*: we could use the FF model here, but for the purposes of 
# this illustration it is more instructive to use RR with very high values 
# for the water permeabilities): 

tissue_ff = dc.ForwardTissueX(water_exchange='FF')
tissue_ff.plot(aif)


# %%
# The indicator concentration in the tissue compartments is not affected by 
# the level of water exchange (top and bottom right), but the magnetization 
# in all 3 compartments is now effectively the same (bottom left). Even the 
# tissue cells, 
# which receive no indicator at all, show the same signal changes over time 
# as the interstitium and blood compartments. This is because, with very high 
# levels of water exchange, the magnetization between all 3 compartments mixes 
# so rapidly that any differences are levelled out instantly. The tissue is 
# well-mixed for water (and therefore water magnetization), although it is not 
# well-mixed for indicator.

# %%
# Now let's consider the cases where one of the barriers is highly permeable 
# for water, and the other is impermeable. First let's look at the case of 
# high transendothelial water exchange and no transcytolemmal water exchange:

tissue_fn = dc.ForwardTissueX(water_exchange='FN')
tissue_fn.plot(aif)

# %%
# As expected, blood and interstitium have the same magnetization throughout 
# and the magnetization of tissue cells is not altered at all. The opposite 
# case is similar:

tissue_nf = dc.ForwardTissueX(water_exchange='NF')
tissue_nf.plot(aif)


# %%
# In this case the tissue cells recieve the same magnetization as the 
# interstitium. 


# %% 
# Water exchange effect on the MR signal
# --------------------------------------
#
# From a measurement perspective, the important question is to what extent 
# water exchange across either barrier affects the measured signal, shown in 
# the top left corner of the plots above. 
# 
# To illustrate the signal differences in more detail, we plot signals in 
# mixed exchange regimes against the extremes of fast and no exchange. For 
# reference we also include a tissue with intermediate water exchange: 

# Build a tissue in an intermediate water exchange regime
tissue_rr = dc.ForwardTissueX(water_exchange='RR')
rr = tissue_rr(aif | {'PSe': 1, 'PSc': 2})

# Generate signals in all regimes
ff = tissue_ff(aif)
nn = tissue_nn(aif)
fn = tissue_fn(aif)
nf = tissue_nf(aif)

# Plot signals against extremes
fig, ax = plt.subplots(1,3, figsize=(15,5))

ax[0].set_title("""No transendothelial exchange \n 
                Fast transcytolemmal exchange""")
ax[1].set_title("""Fast transendothelial exchange \n 
                No transcytolemmal exchange""")
ax[2].set_title("""Restricted transendothelial exchange \n 
                Restricted transcytolemmal exchange""")

ax[0].plot(nf['tS'], nf['S'].flatten(), 'r--', label='Restricted exchange')
ax[1].plot(fn['tS'], fn['S'].flatten(), 'r--', label='Restricted exchange')
ax[2].plot(rr['tS'], rr['S'].flatten(), 'r--', label='Restricted exchange')

for axis in ax:
    axis.plot(ff['tS'], ff['S'].flatten(), 'g-', label='Fast exchange')
    axis.plot(nn['tS'], nn['S'].flatten(), 'b-', label='No exchange')
    axis.set_xlabel('Time (sec)')
    axis.set_ylabel('Signal (a.u.)')
    axis.legend()

plt.show()


# %%
# These figures show clearly that water exchange levels have a measureable 
# effect on signals, and at all times lie between the extremes of no water 
# exchange (blue) and fast water exchange (green). 
#
# However, while the effect of water exchange is detectable, it is 
# comparatively small considering the difference between the blue and green 
# curves represent the extremes. By contrast, changing the exchange rate of 
# the indicator between its extremes of no- and infinite indicator exchange 
# has a more significant impact on the signal:

nx = tissue_rr(aif | {'PS': 0})
ix = tissue_rr(aif | {'PS': 1e-3})
fx = tissue_rr(aif | {'PS': 1e3})

# Plot signals 
fig, ax = plt.subplots(1,1,figsize=(6,5))

ax.set_title('Fast vs no transendothelial indicator exchange')
ax.plot(fx['tS'], fx['S'].flatten(), 'g-', label='Fast indicator exchange')
ax.plot(nx['tS'], nx['S'].flatten(), 'b-', label='No indicator exchange')
ax.plot(ix['tS'], ix['S'].flatten(), 'r--', label='Intermediate indicator exchange')
ax.set_xlabel('Time (sec)')
ax.set_ylabel('Signal (a.u.)')
ax.legend()

plt.show()


# %% 
# Water exchange bias
# -------------------
# As shown above, water exchange is to some extent a second order effect 
# compared to indicator exchange. Nevertheless, making inaccurate assumptions 
# regarding the level of water exchange can lead to large biases in the other 
# measured parameters.
#
# One way to explore the scale of this water exchange bias is by training a 
# tissue that has no water exchange (NN) using data generated by a tissue in 
# fast water exchange:

# Train a NN tissue on the fast-exchange signal and plot results
inverse_nn = dc.InverseTissueX(water_exchange='NN')
inverse_nn.plot(aif | ff)

# %%
# The plot shows that the no-exchange tissue predicts the data with high 
# accuracy. However, the reconstructed magnetization is incorrect for fast 
# exchange tissue, and the reconstructed parameters are biased:

recon = inverse_nn(aif | ff)
truth = tissue_ff.init()
inverse_nn.print(recon, truth)

# %% 
# Removing water exchange bias
# ----------------------------
# Water exchange forms a dangerous source of measurement error because it 
# cannot be detected by comparing the fit to the data. In ideal circumstances, 
# it can be removed by generalizing the model to allow for any level of water 
# exchange. Let's try this and look at the results again:

# Train an RR tissue and plot again
inverse_rr = dc.InverseTissueX(water_exchange='RR')
inverse_rr.plot(aif | ff)

#%%
# Plotting the results now show a practically perfect fit to the data, and the 
# magnetization is correctly transferred to the tissue cells. 
# Also the measurements of the kinetic parameters are more accurate:

recon = inverse_rr(aif | ff)
truth = tissue_ff.init() | {'PSe': np.inf, 'PSc': np.inf}
inverse_rr.print(recon, truth)

# %%
# The relative error in the water permeabilities PSe and PSc can not 
# meaningfully be quantified when the ground truth is infinite, but both 
# values have converged to the upper bound of 100 mL / min / 100mL, which 
# is chosen to be orders of magnitude higher than any physiological regime. 

#%%
# Handling water exchange
# -----------------------
# The above example suggests one strategy of removing water exchange bias, 
# i.e. include water exchange rates as free parameters and get the added 
# benefit of a water exchange measurement. 
# 
# However this may not always be the 
# right approach. The data in this tutorial are noise-free, and therefore even 
# very subtle structure can be exploited to estimate parameters. In noisy data 
# this may not be the case, and one may well be forced to fix parameters that 
# have a relatively small effect on the data in order to improve the precision 
# in others. 
#
# This raises the question where any of the regimes of fast and zero water 
# exchange offers a good approximation to real tissues. For this exercise we 
# simulate a signal with realistic water PS values on the upper 
# end of literature data. We plot the resulting signal against the 
# extremes of fast and no exchange:

# Generate tissue
rr = tissue_rr(aif | {'PSe': 0.05, 'PSc': 1.5})

# Plot signals 
fig, ax = plt.subplots(1,1,figsize=(6,5))

ax.set_title('Restricted water exchange against extremes')
ax.plot(ff['tS'], ff['S'].flatten(), 'g-', label='Fast water exchange')
ax.plot(nn['tS'], nn['S'].flatten(), 'b-', label='No water exchange')
ax.plot(rr['tS'], rr['S'].flatten(), 'r--', label='Restricted water exchange')
ax.set_xlabel('Time (sec)')
ax.set_ylabel('Signal (a.u.)')
ax.legend()

plt.show()

# %%
# With these settings, the restricated water exchange signal is 
# intermediate between fast and no water exchange, but closer to the 
# no exchange regime, despite the fact we have used PSe and PSc values 
# at the upper end of the literature. This suggests a no-exchange 
# limnit is a better approximation for real tissues than a fast exchange 
# limit. All standard approaches for the analysis of DCE-MRI data do 
# the opposite and assume fast water exchange.

# %%
# The impact of water exchange also depends on the imaging sequence, 
# and sequence parameters such as the choice of flip angle. Hence 
# these effects should be taken into account when 
# optimizing the scan protocol. Water exchange sensitivity should be maximized 
# for studies that aim to measure it, and minimized for studies where it is a 
# confounder. 