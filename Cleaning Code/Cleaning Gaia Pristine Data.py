## Data from the Pristine Paper Collecting which combines data from Pristin and Gaia
#   - Pristine Survey XVII - https://ui.adsabs.harvard.edu/abs/2022MNRAS.514.1664Y/abstract

import numpy as np
import pandas as pd

data = pd.read_csv("Data/C-19_fullmember.csv")

cleaned_data = data.dropna(axis=0, how='all', subset=["feh_pr", "feh"])

cleaned_data.to_csv('Cleaned Data/gaia_pristine_c19_stars.csv')