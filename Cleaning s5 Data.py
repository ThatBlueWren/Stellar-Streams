## Data from The S5 Collaboration - https://s5collab.github.io/
#   - Data Release 1, see their PDF for column name and descriptions

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import astropy
from astropy.io import fits

## To-Do:
# compare collected stars in the selected fields with existing lists 

## Cleaning the data
hdul = fits.open('Data/s5_pdr1.fits')   # Opens the fits file
data = hdul[1].data                     # selects the right dataframe
mask_good = data['good_star_pb'] > 0.5  # keeps only stars above a certain quality as defined by the creators (research good cutoff number)
mask_primary = data['primary']          # keeps only 'original' stars, removing repeat data
mask_priority = data['priority'] >= 9   # keeps only stars deemed to be part of stellar streams (values 7-9)

good_star = data[mask_good & mask_primary & mask_priority]  # adds the masks to the data

mask_phoenix = np.char.find(good_star['field'].astype(str), 'Phoenix') >= 0  # keeps only the stars within the Phoenix fields (fields with the phoenix name)

good_phoenix_stars = good_star[mask_phoenix]  # adds the phoenix mask to the data

# Checking that the masks have been applied
#print(len(data), mask_good.sum(), mask_primary.sum(), mask_priority.sum(), mask_phoenix.sum(), len(good_phoenix_stars))  # checks that each mask is working (should contain less entries than the untouched data)

df = pd.DataFrame(good_phoenix_stars.tolist(), columns=good_phoenix_stars.columns.names)  # saving cleaned data to dataframe
df.to_csv('Cleaned Data/s5_phoenix_stars.csv', index=False)  # saving cleaned data to file

hdul.close()  #closes the fits file

