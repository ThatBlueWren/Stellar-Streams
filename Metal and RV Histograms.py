## To-Do:
# - metallicity
# - radial velocity
# - stream width? (more difficult)

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Plotting S5 and Pristine Metallicity Histograms
s5 = pd.read_csv('Cleaned Data/s5_phoenix_stars.csv')
pris = pd.read_csv('Cleaned Data/pristine_c19_stars.csv')
s5_metal = s5["feh50"]
pris_metal = pris["feh"]

#bins = np.linspace(-3.6, -0.3, 20)

#fig_met, ax_met = plt.subplots(1, 2)
#ax_met[0].hist(s5_metal, bins=bins)
#ax_met[0].set_title('Phoenix Stream')

#ax_met[1].hist(pris_metal, bins=bins)
#ax_met[1].set_title('C-19 Stream')

#fig_met.suptitle('Metallicity')
#for a in ax_met:
#    a.set_xlabel('Median Metallicity [Fe/H]')
#    a.set_ylabel('Frequency')

#plt.tight_layout()
#plt.show()


# Plotting S5 and Pristine Radial Velocity Histograms
s5_vel = s5["vel50"]
pris_vel = pris["rv"]

fig_vel, ax_vel = plt.subplots(1, 2)
ax_vel[0].hist(s5_vel); ax_vel[0].set_title('Phoenix Stream')
ax_vel[1].hist(pris_vel); ax_vel[1].set_title('C-19 Stream')

fig_vel.suptitle('Radial Velocity')
for a in ax_vel:
    a.set_xlabel('Median Radial Velocity')
    a.set_ylabel('Frequency')

plt.tight_layout()
plt.show()
