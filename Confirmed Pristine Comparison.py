# anomalies in the radial veleocity could be explained by unconfirmed candidates?
# --> turns out no, the outliers are almost exclusively confirmed candidates!
import pandas as pd

# Cleaning data to keep only confirmed members
df = pd.read_csv('Cleaned Data/pristine_c19_stars.csv')
mask = df['Membership'] == 'Y'
Cleaned_df = df[mask]
#Cleaned_df.to_csv('Cleaned Data/pristine_c19_confirmed.csv')

import matplotlib.pyplot as plt
import numpy as np

pris_a = pd.read_csv('Cleaned Data/pristine_c19_stars.csv')
pris_all = pris_a['rv']
pris_c = pd.read_csv('Cleaned Data/pristine_c19_confirmed.csv')
pris_conf = pris_c['rv']

bins = np.linspace(-300, 100, 20)

fig, ax = plt.subplots()
ax.hist(pris_all, bins=bins, alpha=0.5, label='All C-19 Candidate Members')
ax.hist(pris_conf, bins=bins, alpha=0.5, label='Confirmed C-19 Members')

ax.set_xlabel('Median Radial Velocity')
ax.set_ylabel('Frequency')
ax.set_title('Radial Velocity Comparison')
ax.legend()
plt.show()