from os import listdir
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as const
from ray_optics import *
from nk_helpers import *
from scipy.io import savemat
from scipy.interpolate import make_interp_spline

def plot_setup(fig_x=7.2, fig_y=4.6, dpi=80, SMALL_SIZE=12, MEDIUM_SIZE=14, BIGGER_SIZE=16, bottom_buffer=0.3, left_buffer=0.15):
    plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
    plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
    plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
    plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
    plt.rc('figure', figsize=(fig_x, fig_y))
    plt.rc('figure', dpi=dpi)
    return 

plot_setup(fig_x=7.2, fig_y=4.6)

colors = ['#929591', '#fac205','#c0fb2d','#02ab2e','#7efbb3','#253494']
colors = ['#FB9A29', '#EC7014', '#CC4C02', '#993404', '#662506']
color_gradient = ['#d4ad9d', '#4a352f']
labels = {'b orig':0, 'd':1, 'e':2, 'b':3, 'f':4, 'c':5}
times = {'d':60, 'e':90, 'b':120, 'f':150, 'c':180, 'b orig': 0}
indices = ['b orig', 'd', 'e', 'b', 'f', 'c']

plot_type = 'A'
thickness = 10E-9 #m
theta_i = 0

thicknesses = [48E-9, 50E-9, 59E-9, 69E-9, 71E-9, 62E-9, 73E-9, 77E-9, 79E-9, 91E-9]

DATA_DIRECTORY = "nks/ito3"
LITERATURE_DATA_DIRECTORY = "/home/emmabat/Documents/material_data/material_data_for_COMSOL/"
Nb_n_file = "Nb_n_4k.txt"
Nb_k_file = "Nb_k_4k.txt"
OTHER_INDICES_NAMES = 'nks/Weaver_Nb.csv'

filenames = listdir(DATA_DIRECTORY)

used_indices = []
artists = []

all_y = []
y_lists = []

nb_wl, nb_ns, = read_for_COMSOL(LITERATURE_DATA_DIRECTORY+Nb_n_file)
nb_wl, nb_ks = read_for_COMSOL(LITERATURE_DATA_DIRECTORY+Nb_k_file)
nb_omegas = [wavelength_to_w(nb_wli*1E-9) for nb_wli in nb_wl]

nb_A = [100*absorbance(1, 0, nb_n, nb_k, omega, thickness, theta_i) for nb_n, nb_k, omega in zip(nb_ns, nb_ks, nb_omegas)]
nb_T = [100*transmittance(1, 0, nb_n, nb_k, omega, thickness, theta_i) for nb_n, nb_k, omega in zip(nb_ns, nb_ks, nb_omegas)]
nb_R = [100*reflectance(1, 0, nb_n, nb_k, theta_i) for nb_n, nb_k, omega in zip(nb_ns, nb_ks, nb_omegas)]

nb_data = {
    'nbn': nb_ns,
    'nbk': nb_ks,
    'nbA': nb_A,
    'nbT': nb_T,
    'nbR': nb_R,
    'nbwavelengths': nb_wl,
    'thickness': thickness,
    'angle_of_incidence': theta_i,
    'source': 'Weaver'
}

savemat('nb_optics.mat', nb_data)

low_wl = []
low_A = []
low_T = []
low_R = []
for wl, coeff_A, coeff_T, coeff_R in zip(nb_wl, nb_A, nb_T, nb_R):
    if wl < 1600:
        low_wl.append(wl)
        low_A.append(coeff_A)
        low_T.append(coeff_T)
        low_R.append(coeff_R)
    else:
        break

'''
plt.plot(nb_wl, nb_A, color='black')
plt.xlabel('Wavelengths [nm]')
plt.ylabel('Absorption [%]')
plt.show()

plt.plot(nb_wl, nb_R, color='black')
plt.xlabel('Wavelengths [nm]')
plt.ylabel('Reflection [%]')
plt.show()

plt.plot(nb_wl, nb_T, color='black')
plt.xlabel('Wavelengths [nm]')
plt.ylabel('Transmittance [%]')
plt.show()'''

index_to_nk = {}

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
            omegas = [wavelength_to_w(wavelength*1E-9) for wavelength in wavelengths]
            eps1 = [e1(n, k) for n, k in zip(ns, ks)]
            eps2 = [e2(n, k) for n, k in zip(ns, ks)]

            index = filename[0]
            # uncomment to have corresponding to actual NP layer thicknesses
            #thickness = thicknesses[labels[index]]

            ito_A = [100 * absorbance(1, 0, n, k, omega, thickness, theta_i) for n, k, omega in zip(ns, ks, omegas)]
            print(ito_A)
            ito_R = [100 * reflectance(1, 0, n, k, theta_i) for n, k in zip(ns, ks)]
            ito_T = [100 * transmittance(1, 0, n, k, omega, thickness, theta_i) for n, k, omega in zip(ns, ks, omegas)]
            ito_skindepth = [penetration_depth(k, omega) for k, omega in zip(ks, omegas)]

            ito_data = {
                'n': ns,
                'k': ks,
                'eps1': eps1,
                'eps2': eps2,
                'A': ito_A,
                'R': ito_R,
                'T': ito_T,
                'wavelengths': wavelengths,
                'skindepth': ito_skindepth,
                'thickness': thickness,
                'angle_of_incidence': theta_i
            }
            savemat('ito_optics.mat', ito_data)

            for a, r, t in zip(ito_A, ito_R, ito_T):
                if (a + r + t) - 100 > 1:
                    print('error! a + r + t = '+str(a + r + t))

            color = colors[labels[index]-1]
            #color = colorFader(color_gradient[0], color_gradient[1], (labels[index]-1)/(len(indices)-1))

            if plot_type == 'n':
                y = ns
            elif plot_type == 'k':
                y = ks
            elif plot_type == 'A':
                y = ito_A
            elif plot_type == 'R':
                y = ito_R
            elif plot_type == 'T':
                y = ito_T
            elif plot_type == 'd':
                y = ito_skindepth

            all_y.extend(y)
            y_lists.append(y)
            
            if index in used_indices:
                index_to_nk[index+'ii'] = [ns, ks]
                art, = plt.plot(wavelengths, y, color=color)
            else:
                used_indices.append(index)
                index_to_nk[index] = [ns, ks]
                art, = plt.plot(wavelengths, y, color=color, label=index)
                
            artists.append(art)
    elif filename.endswith('.csv'):
        wavelengths, ns, ks = read_csv(DATA_DIRECTORY + '/' + filename)
        eps1 = [e1(n, k) for n, k in zip(ns, ks)]

        #thickness = 130E-9

        ito_A = [100 * absorbance(1, 0, n, k, omega, thickness, theta_i) for n, k, omega in zip(ns, ks, omegas)]
        ito_R = [100 * reflectance(1, 0, n, k, theta_i) for n, k in zip(ns, ks)]
        ito_T = [100 * transmittance(1, 0, n, k, omega, thickness, theta_i) for n, k, omega in zip(ns, ks, omegas)]

        if plot_type == 'n':
            y = ns 
        elif plot_type == 'k':
            y = ks
        elif plot_type == 'A':
            y = ito_A
        elif plot_type == 'R':
            y = ito_R
        elif plot_type == 'T':
            y = ito_T
        all_y.extend(y)
        plt.plot(wavelengths, y, '--', color='black', label='b orig')

plt.xlabel('Wavelengths [nm]')
if plot_type == 'n':
    plt.ylabel('Refractive index')
    plt.ylim((1, max(all_y) + 0.1))
elif plot_type == 'k':
    plt.ylabel('Extinction coefficient')
    plt.ylim((-0.01, max(all_y) + 0.1))
elif plot_type == 'A':
    ylabel = 'Absorption [%]'
    low_coeff = low_A
elif plot_type == 'R':
    ylabel = 'Reflcection [%]'
    low_coeff = low_R
elif plot_type == 'T':
    ylabel = 'Transmission [%]'
    low_coeff = low_T
elif plot_type == 'd':
    ylabel = 'Skin depth [m]'

plt.ylabel(ylabel)

'''import operator
hl = sorted(zip(artists, [times[i] for i in used_indices]), key=operator.itemgetter(1))
handles, label_order = zip(*hl)

plt.legend()'''

ax = plt.gca()
handles, plot_indices = ax.get_legend_handles_labels()
mapped_labels = [times[i] for i in plot_indices]
labels, handles = zip(*sorted(zip(mapped_labels, handles), key=lambda t: t[0]))
labels = [str(label) + ' s' for label in labels]
ax.legend(handles, labels)

#wavelengths, ns, ks = read_csv('../000c-L.csv')
#plt.plot(wavelengths, ns, color='red')
plt.ylim(ymin = 0)
plt.savefig(plot_type+'_ito'+str(thickness)+'nm_'+str(theta_i)+'.svg')
plt.show()

ns, ks = index_to_nk['b']

ito_A = [100 * absorbance(1, 0, n, k, omega, thickness, theta_i) for n, k, omega in zip(ns, ks, omegas)]
ito_R = [100 * reflectance(1, 0, n, k, theta_i) for n, k in zip(ns, ks)]
ito_T = [100 * transmittance(1, 0, n, k, omega, thickness, theta_i) for n, k, omega in zip(ns, ks, omegas)]


spl = make_interp_spline(low_wl, low_coeff, k=2)

plt.plot(wavelengths, spl(wavelengths)/np.array(ito_A), color='gray', label='ITO nanoparticles')
#plt.plot(low_wl, spl(low_wl), '--', color='black', label='Nb')
#plt.ylim((0, 100))
plt.xlabel('Wavelengths [nm]')
plt.ylabel(ylabel)
plt.legend()
plt.savefig(plot_type+'_ITOvsNb'+str(thickness)+'nm_'+str(theta_i)+'.svg')
plt.show()

itoas = []
itors = []
itots = []
for thick_i in thicknesses:
    ito_A = [100 * absorbance(1, 0, n, k, omega, thick_i, theta_i) for n, k, omega in zip(ns, ks, omegas)]
    ito_R = [100 * reflectance(1, 0, n, k, theta_i) for n, k in zip(ns, ks)]
    ito_T = [100 * transmittance(1, 0, n, k, omega, thick_i, theta_i) for n, k, omega in zip(ns, ks, omegas)]

    itoas.append(ito_A)
    itors.append(ito_R)
    itots.append(ito_T)
'''
for i, (a, thick_i) in enumerate(zip(itoas, thicknesses)):
    color = colorFader('#CEA49B', '#020101', i/(len(thicknesses)-1))
    plt.plot(wavelengths, a, color=color, label=str(thick_i*1E9)+' nm')

plt.xlabel('Wavelengths [nm]')
plt.ylabel('Absorption [%]')
plt.legend()
plt.show()

for i, (r, thick_i) in enumerate(zip(itors, thicknesses)):
    color = colorFader('#CEA49B', '#020101', i/(len(thicknesses)-1))
    plt.plot(wavelengths, r, color=color, label=str(thick_i*1E9)+' nm')

plt.xlabel('Wavelengths [nm]')
plt.ylabel('Reflection [%]')
plt.legend()
plt.show()

for i, (t, thick_i) in enumerate(zip(itots, thicknesses)):
    color = colorFader('#CEA49B', '#020101', i/(len(thicknesses)-1))
    plt.plot(wavelengths, t, color=color, label=str(thick_i*1E9)+' nm')

plt.xlabel('Wavelengths [nm]')
plt.ylabel('Transmission [%]')
plt.legend()
plt.show()'''