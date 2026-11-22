import numpy as np
import dcmri as dc
#
# Generate synthetic test data:
#
time, aif, roi, gt = dc.fake_tissue()
#
# The correct ground truth for ve in model-free analysis is the
# extracellular part of the distribution space:
#
gt['ve'] = gt['vp'] + gt['vi'] if gt['PS'] > 0 else gt['vp']
#
# Build a tissue and set the constants to match the
# experimental conditions of the synthetic test data.
#
tissue = dc.TissueLS(
    dt = time[1],
    sequence = 'SS',
    r1 = dc.relaxivity(3, 'blood','gadodiamide'),
    TR = 0.005,
    FA = 15,
    R10a = 1/dc.T1(3.0,'blood'),
    R10 = 1/dc.T1(3.0,'muscle'),
)
#
# Train the tissue on the data. Since have noise-free synthetic
# data we use a lower tolerance than the default, which is optimized
# for noisy data:
#
tissue.train(roi, aif, n0=10, tol=0.01)
#
# Plot the reconstructed signals along with the concentrations
# and the impulse response function.
#
tissue.plot(roi)
