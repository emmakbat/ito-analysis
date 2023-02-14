import matplotlib.pyplot as plt
from scipy.io import loadmat
import tikzplotlib
from scipy.signal import savgol_filter

filepath_read = 'processed_data/'
filepath_write = 'tikzplots/'
filename1 = 'widewire_tc.mat'
xlabel = 'Temperature [K]'
ylabel = 'Resistivity [Ohms]'

fig_x=7.2
fig_y=4.6
dpi=80
SMALL_SIZE=12
MEDIUM_SIZE=14
BIGGER_SIZE=16
bottom_buffer=0.3
left_buffer=0.15
YlOrBr = ['#FB9A29', '#EC7014', '#CC4C02', '#993404', '#662506']

data1 = loadmat(filepath_read+filename1)

plt.figure()

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
plt.rc('figure', figsize=(fig_x, fig_y))
plt.rc('figure', dpi=dpi)

plt.xlabel(xlabel)
plt.ylabel(ylabel)

plt.plot(data1['t_1000u'][0], data1['offr_1000u'][0])
tikzplotlib.save(filepath_write+'test.tex')