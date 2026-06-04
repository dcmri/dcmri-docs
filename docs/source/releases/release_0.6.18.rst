dcmri 0.6.18
============

This patch fixes a bug which caused gadoxetate relaxivities in hepatocytes to be 
overwritten by plasma relaxivities. The result is that the relaxivity 
correction was not reflected in the rate constants computed by 
gadoxetate DCE-MRI of the liver. Fixing the bug leads to a field-strength 
dependent correction in the absolute values of the uptake 
rates. 

To correct values for uptake rates retrospectively, multiply any 
values derived with earlier dcmri versions with the 
following constants:

- 7T: 1.03
- 4.7T: 0.84
- 3T: 0.65
- 1.5T: 0.55

This update also has moved the documentation in a separate repository 
causing a significantly lighter dcmri package distribution.

Changes
-------

- Bugfix, add copy to not overwrite (`#216 <https://github.com/dcmri/dcmri/pull/216>`_).

Contributors
------------

2 authors added to this release (alphabetically):

- Vendela Andersson (`@vendeladelia <https://github.com/vendeladelia>`_)
- Steven Sourbron (`@plaresmedima <https://github.com/plaresmedima>`_)

