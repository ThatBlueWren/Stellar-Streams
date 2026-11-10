## Data from the Pristine Survey - https://sites.google.com/view/pristinesurvey/home?authuser=0
#   - The Pristine Survey XXVII - https://ui.adsabs.harvard.edu/abs/2025A&A...698A..82Y
#   - Maybe look at Pristine Survey XVI, looks at finding stars within streams, have data but only upon request
#   - Possibly another data source? https://www.nature.com/articles/s41586-021-04162-2#Tab1

import pandas as pd

## To-Do:
# Compare to other sources for C-19! See if you can add any or find other useful data to use

## Cleaning the data
df = pd.read_csv("Data/C-19_memberlist_2025.csv") # reading in data

cleaned_df = df.dropna(subset=["feh"]) # removing entries without Fe/H values

#print(len(df), len(cleaned_df))  # checking cleaning worked (should be size difference)

cleaned_df.to_csv("Cleaned Data/pristine_c19_stars.csv") # saving data to file

## Cleaning data to keep only confirmed members
mask = cleaned_df['Membership'] == 'Y'
member_df = cleaned_df[mask]

member_df.to_csv('Cleaned Data/pristine_c19_confirmed.csv')