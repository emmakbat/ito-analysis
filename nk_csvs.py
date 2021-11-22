import csv
from os import listdir, read
import matplotlib.pyplot as plt

colors = ['#fac205','#c0fb2d','#02ab2e','#7efbb3','#253494']
labels = {'d':0, 'e':1, 'b':2, 'f':3, 'c':4}
times = {'d':60, 'e':90, 'b':120, 'f':150, 'c':180}
indices = ['d', 'e', 'b', 'f', 'c']

DATA_DIRECTORY = "ellips-with-nanoparticles"

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

filenames = listdir(DATA_DIRECTORY)

used_indices = []
artists = []

for filename in filenames:
    if filename.endswith('.csv') and 'int' in filename:
        print(filename)
        if 'np' in filename:
            pass
            '''
            wavelengths, ns, ks = read_csv(DATA_DIRECTORY + '/' + filename)

            index = filename[6]
            color = colors[labels[index]]
            
            if index in used_indices:
                art, = plt.plot(wavelengths, ns, color=color)
            else:
                art, = plt.plot(wavelengths, ns, color=color, label=index)
                used_indices.append(index)
            artists.append(art)'''
        else:
            wavelengths, ns, ks = read_csv(DATA_DIRECTORY + '/' + filename)
            eps1 = [e1(n, k) for n, k in zip(ns, ks)]

            index = filename[3]
            color = colors[labels[index]]
            
            if index in used_indices:
                pass
                art, = plt.plot(wavelengths, eps1, color=color)
            else:
                pass
                art, = plt.plot(wavelengths, eps1, color=color, label=index)
                used_indices.append(index)
            artists.append(art)
    elif filename.endswith('.csv'):
        wavelengths, ns, ks = read_csv(DATA_DIRECTORY + '/' + filename)
        eps1 = [e1(n, k) for n, k in zip(ns, ks)]
        plt.plot(wavelengths, eps1, color='#929591')

plt.xlabel('wavelengths [nm]')
plt.ylabel('refractive index')
#plt.ylabel('extinction coefficient')

'''import operator
hl = sorted(zip(artists, [times[i] for i in used_indices]), key=operator.itemgetter(1))
handles, label_order = zip(*hl)

plt.legend()'''
ax = plt.gca()
handles, plot_indices = ax.get_legend_handles_labels()
mapped_labels = [times[i] for i in plot_indices]
labels, handles = zip(*sorted(zip(mapped_labels, handles), key=lambda t: t[0]))
ax.legend(handles, labels)

#wavelengths, ns, ks = read_csv('../000c-L.csv')
#plt.plot(wavelengths, ns, color='red')

plt.show()