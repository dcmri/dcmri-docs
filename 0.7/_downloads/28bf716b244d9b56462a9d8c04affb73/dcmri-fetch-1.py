import dcmri as dc
import pydmr
#
# # fetch data file
file = dc.fetch('tristan_humans_healthy_rifampicin')
#
# # read data file
data = pydmr.read(file)
