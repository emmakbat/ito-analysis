import scipy.io
import numpy as np
import matplotlib.pyplot as plt
#from csv_plots import read_csv
from scipy.signal import savgol_filter

old_c = scipy.io.loadmat('Tc_data/000c-Tc 2021-06-29 19-59-23 Tc_ITO_EB_2345.mat')
old_n = scipy.io.loadmat('Tc_data/000n-Tc 2021-06-04 10-39-23 Tc_ITO.mat')
old_q = scipy.io.loadmat('Tc_data/000q-Tc 2021-06-29 18-16-06 Tc_ITO_EB_6781.mat')
old_w = scipy.io.loadmat('Tc_data/000w-Tc 2021-07-16 11-15-47 07_16_Tc_ITO_EB_2345.mat')
new_b = scipy.io.loadmat('Tc_data/1-Tc_1678-001bii_cropped.mat')
new_e = scipy.io.loadmat('Tc_data/2-Tc_2345-001eii_cropped.mat')

all_tcs = [old_c, old_n, old_q, old_w] #, new_b, new_e]
labels = ['000c (DAQ 120s)', '000n (NSL 360 s)', '000q (oscope 360 s)', '000w (DAQ 120 s)'] #, '0001b (DAQ 120 s)', '0001e (DAQ 90 s)']

temps = []
normalized = []
for data, label in zip(all_tcs, labels):
    hightemp_r = data['RF'][0][np.argmax(data['TF'][0])]
    
    norm_r = []
    for i, r in enumerate(data['RF'][0]):
        norm_r.append(r/hightemp_r)
        # get index of halfway point in resistivity curve
        if np.abs(r/hightemp_r - 0.5) < 0.0008:
            halfway_index = i 

    halfway_temp = data['TF'][0][halfway_index]
    norm_temps = [temp - halfway_temp for temp in data['TF'][0]]

    temps.append(data['TF'][0])
    normalized.append(norm_r)

    # plot individual Tc measurements
    '''plt.plot(data['TF'][0], data['RF'][0])
    plt.xlabel('Temperature [K]')
    plt.ylabel('Resistivity [Ohms]')
    plt.title(label)
    plt.show()'''

    plt.plot(data['TF'][0], savgol_filter(norm_r, 501, 3), label=label)
    #plt.plot(data['TF'][0], norm_r, label=label)

# plot normalized Tc measurements
plt.title('Smoothed Normalized 4-pt Probe Resistance vs Temperature')
plt.xlabel('Temperature [K]')
plt.ylabel('Normalized Resistivity [Ohms]')
plt.legend()
plt.show()

# read in CSV data for comparison plots (e.g. room-temp vs cryo temp resistivity)
'''samples, sample_dict = read_csv('ITO_summary.csv')

c_data = sample_dict['000c']
n_data = sample_dict['000n']
q_data = sample_dict['000q']
w_data = sample_dict['000w']
bi_data = sample_dict['001bi']
bii_data = sample_dict['001bii']
ei_data = sample_dict['001e']
eii_data = sample_dict['001eii']

all_full_samples = [c_data, n_data, q_data, w_data, bi_data, ei_data]

r_RTs = []
r_cryos = []
annotations = []
for tc_data, full_data, label in zip(all_tcs, all_full_samples, labels):
    r_RT = full_data.Rlong
    
    high_index = np.argmax(tc_data['TF'][0])

    highcryo_r = tc_data['RF'][0][high_index]
    high_temp = tc_data['TF'][0][high_index]

    if r_RT == 'None':
        pass
    else:
        r_RTs.append(r_RT)
        r_cryos.append(highcryo_r)
        annotations.append(label)

plt.title('Room temp vs cryostat (above Tc) resistivity')
plt.xlabel('Room temperature resistivity')
plt.ylabel('Cryo temperature resistivity')
plt.scatter(r_RTs, r_cryos)

for i, txt in enumerate(annotations):
    plt.annotate(txt, (r_RTs[i], r_cryos[i]))

plt.show()'''

