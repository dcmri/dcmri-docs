import numpy as np
import dcmri as dc
#
# Use `fake_brain` to generate synthetic test data:
#
n=64
time, signal, aif, gt = dc.fake_brain(n)
#
# The correct ground truth for ve in model-free analysis is the
# extracellular part of the distribution space:
#
gt['ve'] = gt['ve'] = np.where(gt['PS'] > 0, gt['vp'] + gt['vi'], gt['vp'])
#
# Build a tissue array and set the constants to match the
# experimental conditions of the synthetic test data. We use
# the exact T1-map as baseline values:
#
tissue = dc.TissueLSArray(
    (n,n),
    dt = time[1],
    sequence = 'SS',
    r1 = dc.relaxivity(3, 'blood','gadodiamide'),
    TR = 0.005,
    FA = 15,
    R10a = 1/dc.T1(3.0,'blood'),
    R10 = np.where(gt['T1']==0, 0, 1/gt['T1']),
)
#
# Train the tissue on the data. Since have noise-free synthetic
# data we use a lower tolerance than the default, which is optimized
# for noisy data:
#
tissue.train(signal, aif, n0=10, tol=0.01)
#
# Plot the reconstructed maps, along with the ground truth for reference.
# We set fixed scaling for the parameter maps so they are comparable.
#
vmin = {'Fb':0, 've':0, 'S0':0}
vmax = {'Fb':0.02, 've':0.2, 'S0':np.amax(gt['S0'])}
tissue.plot(vmin=vmin, vmax=vmax, ref=gt)
