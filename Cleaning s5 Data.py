## Data from The S5 Collaboration - https://s5collab.github.io/
#   - Data Release 1, see their PDF for column name and descriptions

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import astropy
from astropy.io import fits

## To-Do:
# Clean data (good_star_pb, remove duplicates by only keeping primary=true, keep priority=7-9, keep only the fields with 'phoenix' in them)
# compare collected stars in the selected fields with existing lists 

hdul = fits.open('Data/s5_pdr1.fits')
data = hdul[1].data
mask_good = data['good_star_pb'] > 0.5  # research good cutoff number
mask_primary = data['primary']

good_star = hdul[1].data[mask_good & mask_primary]

print(len(data), mask_good.sum(), mask_primary.sum(), len(good_star))

#plt.hist(good_star['feh50'], bins=20)
#plt.show()

hdul.close()