import matplotlib.pyplot as plt
import numpy as np
import scipy.constants

ito_einf = 4
ito_mass_eff = 0.35*scipy.constants.m_e

def plasma_freq(n):
    # return plasma frequency of ITO at a given electron concentration
    return np.sqrt(n*(scipy.constants.e)**2/(ito_einf*scipy.constants.epsilon_0*ito_mass_eff))

def freq_to_wavelength(w):
    # return wavelength in nm at a given frequency
    return 2*np.pi*scipy.constants.c*1E9/w

ns = np.arange(1E21, 1E22, 1E19)

plt.plot(ns, plasma_freq(ns))
plt.show()