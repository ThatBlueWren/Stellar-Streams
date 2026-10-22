import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import astropy.units as u
from astropy.coordinates import SkyCoord

# Read in data
C_19 = pd.read_csv('Cleaned Data/pristine_c19_confirmed.csv')
Phoenix = pd.read_csv('Cleaned Data/s5_phoenix_stars.csv')

# ---------- Stream coordinates ----------

# C-19: no published matrix, so fit a great circle to the stars
def stream_frame(ra, dec):
    c = SkyCoord(ra=ra*u.deg, dec=dec*u.deg, frame='icrs')
    v = c.cartesian.xyz.value.T                  # (N, 3) unit vectors

    _, _, vt = np.linalg.svd(v, full_matrices=False)
    pole = vt[2]                                 # normal to best-fit great circle

    m = v.mean(axis=0)
    x = m - (m @ pole) * pole
    x /= np.linalg.norm(x)
    y = np.cross(pole, x)

    phi1 = np.degrees(np.arctan2(v @ y, v @ x))
    phi2 = np.degrees(np.arcsin(np.clip(v @ pole, -1, 1)))
    return phi1, phi2

# Phoenix: rotation matrix from Shipp et al. (2018), Table D.1
R_phoenix = np.array([
    [ 0.59644670,  0.27151332, -0.75533559],
    [-0.48595429, -0.62682316, -0.60904938],
    [ 0.63882686, -0.73032406,  0.24192354],
])

def apply_rotation(ra, dec, R):
    c = SkyCoord(ra=ra*u.deg, dec=dec*u.deg, frame='icrs')
    v = c.cartesian.xyz.value                    # (3, N)
    x, y, z = R @ v
    phi1 = np.degrees(np.arctan2(y, x))
    phi2 = np.degrees(np.arcsin(np.clip(z, -1, 1)))
    return phi1, phi2

C_19['phi1'], C_19['phi2'] = stream_frame(C_19['ra'].values, C_19['dec'].values)
Phoenix['phi1'], Phoenix['phi2'] = apply_rotation(Phoenix['ra'].values, Phoenix['dec'].values, R_phoenix)

print(C_19[['phi1', 'phi2']].describe())
print(Phoenix[['phi1', 'phi2']].describe())

# ---------- Mollweide plot ----------

def moll_xy(phi1_deg, phi2_deg):
    phi1 = (np.asarray(phi1_deg) + 180) % 360 - 180
    return np.radians(phi1), np.radians(np.asarray(phi2_deg))

fig = plt.figure(figsize=(12, 5))
for i, (df, name, col) in enumerate([(C_19, 'C-19', 'C0'),
                                     (Phoenix, 'Phoenix', 'C1')], start=1):
    ax = fig.add_subplot(1, 2, i, projection='mollweide')
    x, y = moll_xy(df['phi1'], df['phi2'])
    ax.scatter(x, y, s=6, color=col)
    ax.grid(True)
    ax.set_title(f'{name} (stream coordinates)')
    ax.set_xlabel(r'$\phi_1$')
    ax.set_ylabel(r'$\phi_2$')

plt.tight_layout()
plt.show()


# https://www.galpy.org/