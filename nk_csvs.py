import csv
from os import listdir, read
import matplotlib.pyplot as plt

colors = ['#fac205','#c0fb2d','#02ab2e','#7efbb3','#253494']
labels = {'d':0, 'e':1, 'b':2, 'f':3, 'c':4}
times = {'d':60, 'e':90, 'b':120, 'f':150, 'c':180}
indices = ['d', 'e', 'b', 'f', 'c']

DATA_DIRECTORY = "../0714_ITOsi_reports_tld"

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

filenames = listdir(DATA_DIRECTORY)

used_indices = []
artists = []

for filename in filenames:
    if filename.endswith('.csv') and 'int' in filename:
        wavelengths, ns, ks = read_csv(DATA_DIRECTORY + '/' + filename)

        index = filename[3]
        color = colors[labels[index]]
        
        if index in used_indices:
            art, = plt.plot(wavelengths, ns, color=color)
        else:
            art, = plt.plot(wavelengths, ns, color=color, label=index)
            used_indices.append(index)

        artists.append(art)
    elif filename.endswith('.csv'):
        wavelengths, ns, ks = read_csv(DATA_DIRECTORY + '/' + filename)
        plt.plot(wavelengths, ns, color='#929591')

plt.xlabel('wavelengths [nm]')
#plt.ylabel('refractive index')
plt.ylabel('extinction coefficient')

import operator
hl = sorted(zip(artists, [times[i] for i in used_indices]), key=operator.itemgetter(1))
handles, label_order = zip(*hl)

plt.legend(handles, label_order)

wavelengths, ns, ks = read_csv('../000c-L.csv')
plt.plot(wavelengths, ns, color='red')

plt.show()