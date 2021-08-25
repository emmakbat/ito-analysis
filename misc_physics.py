import matplotlib.pyplot as plt
import numpy as np
import scipy.constants
from scipy.interpolate import RBFInterpolator

# length/width
CORRECTION_COLUMNS = np.tile(np.asarray([1, 2, 3, 4]), (11, 1)).flatten()
# width/spacing
CORRECTION_ROWS = np.tile(np.asarray([[1], [1.25], [1.5], [1.75], [2], [2.5], [3], [4], [5], [7.5], [10]]), (1, 4)).flatten()
CORRECTION_TABLE = np.asarray(
    [
        [0, 0, 0.2204, 0.2205],
        [0, 0, 0.2751, 0.2751],
        [0, 0.3263, 0.3286, 0.3286],
        [0, 0.3794, 0.3803, 0.3803],
        [0, 0.4292, 0.4297, 0.4297],
        [0, 0.5192, 0.5194, 0.5194],
        [0.5422, 0.5957, 0.5958, 0.5958],
        [0.6870, 0.7115, 0.7115, 0.7115],
        [0.7744, 0.7887, 0.7887, 0.7887],
        [0.8846, 0.8905, 0.8905, 0.8905],
        [0.9313, 0.9345, 0.9345, 0.9345]
    ]
).flatten()

ito_einf = 4
ito_mass_eff = 0.35*scipy.constants.m_e

def plasma_freq(n):
    # return plasma frequency of ITO at a given electron concentration
    return np.sqrt(n*(scipy.constants.e)**2/(ito_einf*scipy.constants.epsilon_0*ito_mass_eff))

def freq_to_wavelength(w):
    # return wavelength in nm at a given frequency
    return 2*np.pi*scipy.constants.c*1E9/w

def correction_factor(length, width, spacing=0.2):
    '''
    length = long side of sample [cm]
    width = short side of sample [cm]
    spacing = space between 4 pt probe pins [cm]

    returns correction factor for a four point probe measurement of rectangular sample
    '''
    correction_function = RBFInterpolator(
        np.stack([CORRECTION_COLUMNS, CORRECTION_ROWS], -1), CORRECTION_TABLE, kernel='cubic')
    column = length/width 
    row = width/spacing 

    return correction_function(np.stack([[column], [row]], -1))[0]

#ns = np.arange(1E21, 1E22, 1E19)

#plt.plot(ns, freq_to_wavelength(plasma_freq(ns)))
#plt.show()

print(correction_factor(1, 0.275))