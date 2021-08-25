import scipy.io
import numpy as np
import matplotlib.pyplot as plt
from os import listdir
#from csv_plots import read_csv
from scipy.signal import savgol_filter

DATA_DIRECTORY = "Tc_0816"

def plotSingleTcData(data, label='Tc Measurement'):
    plt.plot(data['TF'][0], data['RF'][0], linestyle='None', marker='o', markersize=3)
    plt.xlabel('Temperature [K]')
    plt.ylabel('Resistivity [Ohms]')
    plt.title(label)
    plt.show()

def plotMultipleTcData(all_tcs, labels=[], normalize_R=True, normalize_temp=False, 
    smoothing=False, title='Resistivity vs Temperature'):
    '''
    plot multiple Tc measurements at once
    all_tcs = Tc measurement imported from MAT file with scipy.io
    labels = labels for plotting
    normalize_R = boolean; if True, plots with Rs normalized to R at highest meas. T
    normalize_temp = boolean; if True, plots with temps shifted so R(Tnorm=0) = 0.5 Rmax
    '''

    # to be list of lists of temp + R
    temps = []
    resistivities = []

    if len(labels) == 0:
        labels = range(1, len(all_tcs))

    for data, label in zip(all_tcs, labels):
        hightemp_r = data['RF'][0][np.argmax(data['TF'][0])]
        # set resistivity to normalized RF data
        rtc = 0

        if normalize_R:
            norm_r = []
            for i, r in enumerate(data['RF'][0]):
                norm_r.append(r/hightemp_r)
                # get index of halfway point in resistivity curve
                if np.abs(r/hightemp_r - 0.5) < np.abs(rtc/hightemp_r - 0.5):
                    rtc = r
                    halfway_index = i 
            
            resistivity = norm_r
            ylabel = 'Normalized Resistivity [Ohm]'
        # else set resistivity to RF data
        else:
            resistivity = data['RF'][0]
            ylabel = 'Resistivity [Ohm]'
            for r in data['RF'][0]:
                if np.abs(r/hightemp_r - 0.5) < np.abs(rtc/hightemp_r - 0.5):
                    rtc = r
                    halfway_index = i 
        
        print(label + ' Tc: ')
        print(data['TF'][0][halfway_index])

        if normalize_temp:
            halfway_temp = data['TF'][0][halfway_index]
            temp = [temp - halfway_temp for temp in data['TF'][0]]
            xlabel = 'Normalized Temperature [K]'
        else:
            temp = data['TF'][0]
            xlabel = 'Temperature [K]'

        temps.append(temp)
        resistivities.append(resistivity)

        if smoothing:
            plt.plot(temp, savgol_filter(resistivity, 501, 3), label=label)
        else:
            plt.plot(temp, resistivity, label=label)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()

filenames = listdir(DATA_DIRECTORY)

all_tc_data = []
labels = []
for filename in filenames:
    if filename.endswith('.mat'):
        tc_data = scipy.io.loadmat(DATA_DIRECTORY + '/' + filename)
        label = filename[-8:-4]
        plotSingleTcData(tc_data, 'Tc Measurement 0731 Pads '+ label)

        all_tc_data.append(tc_data)
        labels.append(label)

plotMultipleTcData(all_tc_data, labels)

times = [60, 90, 120, 150, 180]
tci = [np.nan, np.nan, 1.379, np.nan, 1.381]
tcii = [1.368, 1.95, 1.424, 1.846, 1.56]

plt.scatter(times, tci)
plt.scatter(times, tcii)
plt.ylim(ymin=0)
plt.xlim(xmin=0)
plt.xlabel('Intercalation time [s]')
plt.ylabel('Tc [K]')
plt.show()