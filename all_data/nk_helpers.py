import csv
import matplotlib as mpl
import numpy as np
import scipy.constants as const


def read_for_COMSOL(filename):
    wavelengths = []
    y = []
    with open(filename) as file:
        data = file.readlines()
        for line in data:
            data_list = line.split()
            wavelengths.append(float(data_list[0]))
            y.append(float(data_list[1]))
    return wavelengths, y


def read_riinfo(filename):
    with open(filename) as csvfile:
        read = csv.reader(csvfile)

        wavelengths = []
        ns = []
        ks = []

        for i, row in enumerate(read):
            if i == 0:
                pass 
            else:
                wavelengths.append(1E3*float(row[0]))
                ns.append(float(row[1]))
                ks.append(float(row[2]))
    return wavelengths, ns, ks

def read_csv(filename):
    with open(filename) as csvfile:
        read = csv.reader(csvfile)

        wavelengths = []
        ns = []
        ks = []

        for i, row in enumerate(read):
            if i == 0 or i == 1:
                pass 
            else:
                wavelengths.append(float(row[0]))
                ns.append(float(row[1]))
                ks.append(float(row[3]))

    return wavelengths, ns, ks 

def e1(n, k):
    '''wavelength [um]

    computes real permittivity at wavelength by computing n&k
    according to the optical model
    '''
    return n**2 - k**2

def e2(n, k):
    '''wavelength [um]

    computes imaginary permittivity at wavelength by computing n&k
    according to the optical model
    '''
    return 2*n*k

def wavelength_to_w(wavelength):
    return 2*np.pi*const.c/wavelength

def colorFader(c1, c2, mix=0):
    '''
    credit to Markus Dutschke on Stack Overflow for this one
    '''
    c1 = np.array(mpl.colors.to_rgb(c1))
    c2 = np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_hex((1-mix)*c1 + mix*c2)