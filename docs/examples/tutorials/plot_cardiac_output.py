"""
==============
Cardiac output
==============

This tutorial illustrates how the Aorta model `~dcmri.InverseAorta` 
can be used to measure the cardiac output from an arterial input 
function (AIF). 

An AIF is typically used in DC-MRI to derive input concentrations 
for a tissue model. However, the AIF signal also encodes properties 
of the circulation, which can be derived by fitting a model of the 
circulation to the AIF.

We will illustrate the idea by measuring the (average) cardiac output of 
subjects used to derive a popular literature-based input function  
from `Parker et al 2006 <https://onlinelibrary.wiley.com/doi/full/10.1002/mrm.21066>`_. 
It is implemented in `dcmri` as the function `~dcmri.parker` and the 
module `~dcmri.Parker`.
"""

# %%
# We'll start by importing the package:
import dcmri as dc

# %%
# ... and generating the population-average AIF. We use the default 
# settings from the original paper, so no need to provide arguments:
aif = dc.Parker()()

# %%
# In order to apply the module `~dcmri.InverseAorta`, we need to 
# first configure it, and then set the input parameters. 
# The default configuration
# is mostly fine but we will choose a chain model for the heart-lung 
# system to create a more realistic first pass. Since the data are 
# acquired over several minutes we will allow for extravasation in 
# the organs, and we will also allow measured values for the blood 
# relaxation so we don't have to rely on preset literature values:
aorta = dc.InverseAorta(
    heartlung='chain', 
    organs='2cxm', 
    baseline='measured',
)

# %%
# Most inputs, such as sequence parameters, are already returned as 
# part of the aif, so we only need to provide values for the missing 
# inputs. Let's see what they are:
missing_data = aorta.inputs() - aif.keys()
dc.print_quantities(missing_data)

# %%
# The physiological parameters will be derived by the function, so we 
# can leave them to their defaults; for the other parameters 
# the defaults are OK too, so no need to make changes

# %%
# We can now fit the model to the data:
result = aorta(aif)

# %%
# Before we look at the results, let's check that the fit has 
# converged to the correct solution. To do this, we 
# first update the data with the new optimized values, 
# and then plot it with the ground truth concentrations as reference:
aif |= result['popt']
aorta.plot(aif)

# %%
# The fit looks good so we can interpret the results. Let's 
# print them out:
dc.print_quantities(result['popt'])

# %%
# The measured cardiac output is high: a value of 220 mL/sec 
# corresponds to 13.2 L/min, which is more than twice the typical 
# value in healthy volunteers. This is in fact a known property of 
# this particular population-average AIF. It has been observed before by 
# `Yang et al (2009) <https://onlinelibrary.wiley.com/doi/10.1002/mrm.21912>`_,
# though their exact estimate was less elevated (10.5 L/min). 


# sphinx_gallery_start_ignore
# sphinx_gallery_thumbnail_number = -1
# sphinx_gallery_end_ignore

