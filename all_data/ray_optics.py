import scipy.constants as const
import numpy as np

'''
Sources: Optics of Thin Solid Films (Heavens, 1960), 
         Etude Theorique des Proprietes Optiques des Couches Minces Transparentes (P. Bousquet, 1957)
         Optics (E. Hecht)
'''

def absorption_coeff(k, omega):
    return 2*omega*k/const.c 

def transmittance_90(n1, k1, n2, k2, omega, thickness):
    r = reflectance_90(n1, k1, n2, k2)
    return (1 - r) * np.exp(-absorption_coeff(k2, omega)*thickness)

def reflectance_90(n1, k1, n2, k2):
    return ((n1 - n2)**2 + (k1 - k2)**2)/((n1 + n2)**2 + (k1 + k2)**2)

def absorbance_90(n1, k1, n2, k2, omega, thickness):
    r = reflectance_90(n1, k1, n2, k2)
    t = transmittance_90(n1, k1, n2, k2, omega, thickness)
    return 1 - r - t

def penetration_depth(k, omega):
    return 1/absorption_coeff(k, omega)


def transmittance(n1, k1, n2, k2, omega, thickness, theta_i=0):
    r = reflectance(n1, k1, n2, k2, theta_i)
    distance = distance_in_film(n2, k2, r, thickness, theta_i)
    return (1 - r) * np.exp(-absorption_coeff(k2, omega)*distance)


def absorbance(n1, k1, n2, k2, omega, thickness, theta_i=0):
    r = reflectance(n1, k1, n2, k2, theta_i)
    t = transmittance(n1, k1, n2, k2, omega, thickness, theta_i)
    return 1 - r - t

def gammas_reflectance(gamma1, gamma2):
    '''
    computes the reflection coefficient from the gamma velocity factors (Bousquet 1957)
    '''
    return (gamma1 - gamma2)/(gamma1 + gamma2)

def alpha1(theta_i):
    '''
    returns the "alpha" velocity factor for the incident wave in air
    '''
    return np.sin(theta_i)/const.c

def gamma2(n, k, theta_i):
    '''
    computes the "gamma" velocity factor for the transmitted wave
    '''
    return np.sqrt((np.abs(n + 1j*k)**2 - np.sin(theta_i)**2)/const.c**2)

def gamma1(theta_i):
    '''
    computes the "gamma" velocity factor for the incident wave in air
    '''
    return np.cos(theta_i)/const.c 

def reflectance(n1, k1, n2, k2, theta_i=0):
    '''
    computes the reflectance from gamma velocity factors
    '''
    y1 = gamma1(theta_i)
    y2 = gamma2(n2, k2, theta_i)
    return np.abs(gammas_reflectance(y1, y2))**2

def compute_costheta_t(n, k, r, theta_i):
    '''
    computes the transmitted angle from reflection coefficients
    '''
    real_r = np.real(r)
    return np.cos(theta_i)*(-np.sqrt(n**2 + k**2 - k**2*real_r**2) + real_r*n)/((real_r - 1)*(k**2 + n**2))

def distance_in_film(n, k, r, thickness, theta_i):
    return thickness/compute_costheta_t(n, k, r, theta_i)