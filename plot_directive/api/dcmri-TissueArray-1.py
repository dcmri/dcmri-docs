import numpy as np
import dcmri as dc
#
# Use `fake_brain` to generate synthetic test data:
#
n=8
time, signal, aif, gt = dc.fake_brain(n)
#
# Build a tissue array and set the constants to match the
# experimental conditions of the synthetic test data:
#
shape = (n,n)
tissue = dc.TissueArray(
    shape,
    sequence = 'SS',
    aif = aif,
    dt = time[1],
    r1 = dc.relaxivity(3, 'blood', 'gadodiamide'),
    TR = 0.005,
    FA = 15,
    n0 = 10,
)
#
# Train the tissue on the data:
#
tissue.train(time, signal)
#
# Plot the reconstructed maps, along with their standard deviations
# and the ground truth for reference:
#
tissue.plot(time, signal, ref=gt)
