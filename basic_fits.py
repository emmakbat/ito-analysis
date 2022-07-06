from asyncore import read
from scipy.stats import linregress 
import numpy as np
import matplotlib.pyplot as plt
import csv

filename = 'data/ITO3model_constants.csv'

SMALL_SIZE = 12
MEDIUM_SIZE = 14
BIGGER_SIZE = 16

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

def read_csv(filename):
    with open(filename) as csvfile:
        read = csv.reader(csvfile)
        labels = []
        vals = []
        for i, row in enumerate(read):
            if i == 0:
                labels = row 
                for label in labels:
                    vals.append([])
            else:
                for i, cell in enumerate(row):
                    if i != 1:
                        cell = float(cell)
                    vals[i].append(cell)
    return labels, vals

def print_plot_linregress(x, y, xlabel, ylabel):
    result = linregress(x, y)
    predicted_y = [xi*result.slope + result.intercept for xi in x]

    print(ylabel)
    print(f"R-squared: {result.rvalue**2:.6f}")
    print(f"p-value: {result.pvalue:.6f}")
    print(f"slope: {result.slope:.6f} +/- {result.stderr:.6f}")
    print(f"intercept: {result.intercept:.6f} +/- {result.intercept_stderr:.6f}")

    plt.plot(x, predicted_y, color='gray', label='Regression model')
    plt.plot(x, y, 'o', color='black', label='Measured data')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()

labels, vals = read_csv(filename)
labels = ['n/a', 'n/a', 'Bulk thickness [nm]', 'Nanoparticle thickness [nm]', 'Lorentz oscillator strength', 'Lorentz oscillator position [eV]',
    'Lorentz oscillator width [eV]', 'Drude oscillator position [eV]', 'Drude oscillator width [eV]',
    'Lorentz oscillator strength', 'Lorentz oscillator position [eV]', 'Lorentz oscillator width [eV]', 'Core permittivity']
times = vals[0]
for i, label in enumerate(labels):
    if i == 0 or i == 1:
        pass 
    else:
        y = vals[i]
        print_plot_linregress(times, y, 'Reduction time [s]', label)