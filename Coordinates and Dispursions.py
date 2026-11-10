import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import astropy.units as u
from astropy.coordinates import SkyCoord
from scipy.optimize import minimize 

# Read in data
C_19 = pd.read_csv('Cleaned Data/the_one_c19_to_rule_them_all.csv')
Phoenix = pd.read_csv('Cleaned Data/s5_phoenix_stars.csv')

## Figure Options:
show_mollweide = False
show_width     = False 
show_rv        = True  


## Making the stream coordinates
# C-19: no published matrix, so fit a great circle to the stars
def stream_frame(ra, dec):
    c = SkyCoord(ra=ra*u.deg, dec=dec*u.deg, frame='icrs')  # makes the skycoords, u.deg signifies the units used
    v = c.cartesian.xyz.value.T     # turns positions into 3D unit vectors --> 'cartesian' converts to cartesian, 'xyz' builds each column into the matrix, 'value' removes the units for a plain numpy array, 'T' transposes the matrix

    _, _, vt = np.linalg.svd(v, full_matrices=False)    # finds the normal to the plane (the section with the least variation)
    pole = vt[2]                                 # defines the normal as the pole

    m = v.mean(axis=0)  # average star direction
    x = m - (m @ pole) * pole   # removes the part of 'm' that sticks out of the plane
    x /= np.linalg.norm(x)  # projection of mean star direction onto great circle plane
    y = np.cross(pole, x)   # takes the cross product of x to get another axis, alongside 'x' and 'pole'

    phi1 = np.degrees(np.arctan2(v @ y, v @ x)) # converts our x and y axis's into the new axis
    phi2 = np.degrees(np.arcsin(np.clip(v @ pole, -1, 1)))  # converts the pole axis into the new axis
    R = np.vstack([x, y, pole]) # creates matrix with the new axes
    return phi1, phi2, R

# Phoenix: rotation matrix from Shipp et al. (2019), Table D.1 - https://arxiv.org/pdf/1907.09488
R_phoenix = np.array([
    [ 0.59644670,  0.27151332, -0.75533559],
    [-0.48595429, -0.62682316, -0.60904938],
    [ 0.63882686, -0.73032406,  0.24192354],
])

def apply_rotation(ra, dec, R):
    c = SkyCoord(ra=ra*u.deg, dec=dec*u.deg, frame='icrs')  #makes the skycoords
    v = c.cartesian.xyz.value   # turns the positions into the 3D unit vectors
    x, y, z = R @ v # rotating the stars into the stream frame
    phi1 = np.degrees(np.arctan2(y, x)) # makes the new coords
    phi2 = np.degrees(np.arcsin(np.clip(z, -1, 1))) # makes the new coords
    return phi1, phi2

# defining the axes for each
C_19['phi1'], C_19['phi2'], R_c19 = stream_frame(C_19['ra'].values, C_19['dec'].values)
Phoenix['phi1'], Phoenix['phi2'] = apply_rotation(Phoenix['ra'].values, Phoenix['dec'].values, R_phoenix)


## Making the Mollwiede plot
def moll_xy(phi1_deg, phi2_deg):
    phi1 = (np.asarray(phi1_deg) + 180) % 360 - 180 # need longitude in radians from -Pi to Pi
    return np.radians(phi1), np.radians(np.asarray(phi2_deg))

if show_mollweide:
    fig = plt.figure(figsize=(12, 5))
    for i, (df, name, col) in enumerate([(C_19, 'C-19', 'C0'),  # loops over the two streams, giving the dataframe, name, and colour ('enumerate' adds an index counter to each item in returning pairs, used to determine which stream they belong to)
                                        (Phoenix, 'Phoenix', 'C1')], start=1):
        ax = fig.add_subplot(1, 2, i, projection='mollweide')   # creates subplots 'i' in 2 columns using mollweide projection
        x, y = moll_xy(df['phi1'], df['phi2'])  # converts the streams angles for viewing
        ax.scatter(x, y, s=6, color=col)    # scatters the stars
        ax.grid(True)
        ax.set_title(f'{name} (stream coordinates)')
        ax.set_xlabel(r'$\phi_1$')
        ax.set_ylabel(r'$\phi_2$')
    plt.tight_layout()
    plt.show()

## Spline fitting
# Stream Width
C_19 = C_19[C_19['source_id'] != 2288313499629002624] # seemingly positional outlier, even though 'confirmed' member

c19_coeffs = np.polyfit(C_19['phi1'], C_19['phi2'], deg=3)
c19_fit = np.poly1d(c19_coeffs)
C_19['phi2_resid'] = C_19['phi2'] - c19_fit(C_19['phi1'])

phoenix_coeffs = np.polyfit(Phoenix['phi1'], Phoenix['phi2'], deg=3)
phoenix_fit = np.poly1d(phoenix_coeffs)
Phoenix['phi2_resid'] = Phoenix['phi2'] - phoenix_fit(Phoenix['phi1'])

if show_width:
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    for row, (df, fit, name) in zip(axes, [(C_19, c19_fit, 'C-19'),
                                            (Phoenix, phoenix_fit, 'Phoenix')]):
        xs = np.linspace(df['phi1'].min(), df['phi1'].max(), 500)
        row[0].scatter(df['phi1'], df['phi2'], s=6)
        row[0].plot(xs, fit(xs), 'r')
        row[0].set_title(f'{name}: fit')
        row[0].set_xlabel(r'$\phi_1$ (deg)'); row[0].set_ylabel(r'$\phi_2$ (deg)')

        row[1].scatter(df['phi1'], df['phi2_resid'], s=6)
        row[1].axhline(0, color='r')
        row[1].set_title(f'{name}: residual vs $\\phi_1$')
        row[1].set_xlabel(r'$\phi_1$ (deg)'); row[1].set_ylabel('residual (deg)')

        row[2].hist(df['phi2_resid'], bins=30)
        row[2].set_title(f'{name}: residual distribution')
        row[2].set_xlabel('residual (deg)')
    plt.tight_layout(); plt.show()


# Radial velocity dispursion
Phoenix = Phoenix[Phoenix['name'] != '4914223274240174208'] # extreme rv outlier (-1200)

C_19 = C_19.dropna(subset=["rv"])

c19_rv_coeffs = np.polyfit(C_19['phi1'], C_19['rv'], deg=3)
c19_rv_fit = np.poly1d(c19_rv_coeffs)
C_19['rv_resid'] = C_19['rv'] - c19_rv_fit(C_19['phi1'])

phoenix_rv_coeffs = np.polyfit(Phoenix['phi1'], Phoenix['vel_calib'], deg=3)
phoenix_rv_fit = np.poly1d(phoenix_rv_coeffs)
Phoenix['rv_resid'] = Phoenix['vel_calib'] - phoenix_rv_fit(Phoenix['phi1'])

if show_rv:  
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    for row, (df, fit, name, col) in zip(axes, [(C_19, c19_rv_fit, 'C-19', 'rv'),
                                                 (Phoenix, phoenix_rv_fit, 'Phoenix', 'vel_calib')]):
        xs = np.linspace(df['phi1'].min(), df['phi1'].max(), 500)

        row[0].scatter(df['phi1'], df[col], s=6)
        row[0].plot(xs, fit(xs), 'r')
        row[0].set_title(f'{name}: RV fit')
        row[0].set_xlabel(r'$\phi_1$ (deg)'); row[0].set_ylabel('RV (km/s)')

        row[1].scatter(df['phi1'], df['rv_resid'], s=6)
        row[1].axhline(0, color='r')
        row[1].set_title(f'{name}: RV residual vs $\\phi_1$')
        row[1].set_xlabel(r'$\phi_1$ (deg)'); row[1].set_ylabel('residual (km/s)')

        row[2].hist(df['rv_resid'], bins=30)
        row[2].set_title(f'{name}: RV residual distribution')
        row[2].set_xlabel('residual (km/s)')
    plt.tight_layout(); plt.show()